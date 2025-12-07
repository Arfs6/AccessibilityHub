"""Automate seting up servers and deploying code."""

import json
import logging
import sys
from collections.abc import Generator

from fabric import Connection, task

log = logging.getLogger()
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
log.addHandler(consoleHandler)
log.setLevel(logging.INFO)

try:
    with open('servers_config.json') as fileObj:
        config = json.load(fileObj)
except FileNotFoundError:
    log.exception(
        'Could not find the servers_config.json file. Make sure you have it and it is in the same directory with your fab file.'
    )
    sys.exit()
except json.JSONDecodeError:
    log.exception('You have a syntax error in your server_config.json file ')
    sys.exit()


def allServers() -> Generator:
    """Yields Connection objects for servers."""
    for server in config['servers']:
        if server.get('type') == 'lb':
            continue
        con = Connection(
            host=server['host'], user=server['user'], connect_kwargs={'key_filename': config['private_key']}
        )
        yield con


def _installPython(c):
    """Installs python and all it's dependencies."""
    c.run('sudo apt-get update')
    c.run('sudo add-apt-repository ppa:deadsnakes/ppa')
    c.run('sudo apt-get install python3.11 -y')
    c.run('curl https://bootstrap.pypa.io/get-pip.py | sudo python3.11')
    extras = ['python3.11-dev', 'python3.11-distutils ', 'python3.11-venv']
    c.run('sudo apt-get install -y ' + ' '.join(extras))


@task
def installPython(c):  # noqa: ARG001
    """Iterates through all servers and installs python."""
    for con in allServers():
        _installPython(con)


def _setupPythonEnv(c):
    """Clones the repo and creates a virtual environment"""
    with c.cd('~'):
        c.run('git clone https://github.com/arfs6/AccessibilityHub')
    with c.cd('~/AccessibilityHub'):
        c.run('python3.11 -m venv env')


@task
def setupPythonEnv(c):  # noqa: ARG001
    """setups python environment in both servers."""
    for con in allServers():
        _setupPythonEnv(con)


def _setupGunicorn(c: Connection):
    """Sets up the gunicorn socket and service.d script."""
    c.put('systemd/gunicorn.socket', remote='/tmp')  # noqa: S108
    c.put('systemd/gunicorn.service', remote='/tmp')  # noqa: S108
    with c.cd('/etc/systemd/system/'):
        c.run('sudo mv /tmp/gunicorn.socket ./')
        c.run('sudo mv /tmp/gunicorn.service ./')
    c.run('sudo systemctl start gunicorn.socket')
    c.run('sudo systemctl enable gunicorn.socket')
    c.run('sudo systemctl daemon-reload')
    c.run('sudo systemctl restart gunicorn.socket')


@task
def setupGunicorn(c):  # noqa: ARG001
    """Setup gunicorn in both servers."""
    for con in allServers():
        _setupGunicorn(con)


def _setupNginx(c: Connection):
    """Setup nginx configuration and service."""
    c.run('sudo apt-get update')
    c.run('sudo apt-get install nginx -y')
    c.put('nginx/accessibilityhub', remote='/tmp')  # noqa: S108
    with c.cd('/etc/nginx/'):
        c.run('sudo mv /tmp/accessibilityhub sites-available')
        c.run('sudo ln -fs /etc/nginx/sites-available/accessibilityhub /etc/nginx/sites-enabled/default')
        if c.run('sudo nginx -t').return_code != 0:
            log.error('Nginx configuration failed\nFile at deploy/nginx/accessibilityhub.')
            sys.exit()
    c.run('sudo service nginx restart')


@task
def setupNginx(c):  # noqa: ARG001
    """Setup nginx on both servers."""
    for idx, con in enumerate(allServers()):
        log.info('Setting up nginx in server #%s', idx)
        _setupNginx(con)


@task
def setupUfw(c):  # noqa: ARG001
    """Setup ufw."""
    for con in allServers():
        con.run('sudo ufw allow ssh')
        con.run('sudo ufw allow 3306')
        con.run("sudo ufw allow 'Nginx HTTP'")
        con.run('sudo ufw enable')
        con.run('sudo ufw reload')


@task
def setupLoadBalancer(c):  # noqa: ARG001
    """Configures haproxy on load balancer server and enable firewall."""
    lbServer: dict | None = None
    for server in config['servers']:
        if server.get('type') == 'lb':
            lbServer = server
            break
    if lbServer is None:
        log.error('No load balancer in server config file.')
        return
    con = Connection(
        host=lbServer['host'], user=lbServer['user'], connect_kwargs={'key_filename': config['private_key']}
    )
    con.sudo('apt-get update')
    con.sudo('apt-get install haproxy -y')
    # enable init script for haproxy.
    # Make sure running the command twice has no effect.
    con.sudo('mv /etc/haproxy/haproxy.cfg{,.old}')
    con.put('haproxy/haproxy.cfg', remote='/tmp')  # noqa: S108
    con.sudo('mv /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg')
    con.sudo('service haproxy restart')


@task
def setupServers(c):  # noqa: ARG001
    """Install everything we need to run our django app."""
    for con in allServers():
        _installPython(con)
        _setupPythonEnv(con)
        _setupNginx(con)
        _setupGunicorn(con)
        setupUfw(con)


@task
def updatePipDependencies(c):  # noqa: ARG001
    """Installs new pip dependencies on server."""
    for con in allServers():
        with con.cd('~/AccessibilityHub'):
            con.run('git pull')
            con.run('env/bin/python -m pip install -r requirements.txt')


@task
def deploy(c):  # noqa: ARG001
    """Deploys a new version of Accessibility Hub."""
    for con in allServers():
        with con.cd('~/AccessibilityHub'):
            con.run('git pull')
        with con.cd('~/AccessibilityHub/src/accessibilityHub'):
            con.run('../../env/bin/python manage.py makemigrations')
            con.sudo('../../env/bin/python manage.py migrate')
        con.run('sudo systemctl restart gunicorn.socket')
        con.sudo('systemctl restart gunicorn')
