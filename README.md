## Accessibility Hub

## A community focused on accessibility

This project creates a platform for discussions on topics related to the accessibility of digital and physical tools, including a section where users can review tools by submitting a rating and a comment.

Live demo at: <https://arfs6.pythonanywhere.com>

> Accessibility is not just about screen readers and blindness. To me, a tool is accessible when I can work with the tool independently. On the other hand, a tool isn't accessible when it requires extra steps, extra tools or extra resources for me to be able to use it.

## Content of This Repository

This repository has a basic implementation of the AccessibilityHub website. This include the [django](#django) project, the frontend assets (html, css and js) and the installation scripts.

## Running The Project Locally

You need [hatch](#hatch) to be able to run the website locally. Make sure you have it [installed](https://hatch.pypa.io/latest/install/) on your machine.

### Starting The Server

1. **Clone this repo**: `git clone https://github.com/arfs6/AccessibilityHub`
2. **Switch to the repo directory**: `cd AccessibilityHub`
3. **Create secret key for .env**: `hatch run random-secret-key >> .env`
4. **Start the development server**: `hatch run src/accessibilityHub/manage.py runserver`

Wait for hatch to finish setting up the project. Then you can open your browser and type `localhost:8000` in the address bar to open the website.

### Managing Database

In order to make any database operations, you'll need to generate and execute the schema using django's `manage.py` utility tool.

1. **Generate schema**: `hatch run src/accessibilityHub/manage.py makemigrations`
2. **Execute schema**: `hatch run src/accessibilityHub/manage.py migrate`

Running the above commands will allow you to create and access data stored in the database, like user accounts.

### Running Tests and Ruff

1. **Test**: `hatch run src/accessibilityHub/manage.py test tests`
2. **Ruff (linting and formatting)**: `hatch fmt`

`mypy` is supposed to be the static type checker, but I haven't tried it yet.

## Project Disassembling

Here are the key components of Accessibility Hub:

- [Django](#django)
- [Gunicorn](#gunicorn)
- [Nginx](#nginx)
- [MySQL and SQLite](#mysql-and-sqlite)
- [HTMX](#htmx)
- [Fabric](#fabric)
- [Hatch](#hatch)

### Django {#django}

Accessibility hub is built with the [django](https://www.djangoproject.com) framework. I chose django for its "batteries included" nature, it comes with most of the things I need to build a backend.

There are four (4) apps in the django project:

- `core`: Shared logic, templates and general pages.
- `discussions`: Handle all discussions related features.
- `review`: Handles all reviews related features.
- `api`: Has mini views and templates. This may be removed in the future.

The [`django-htmx`](https://django-htmx.readthedocs.io/en/latest/) middleware was added to streamline htmx usage.

### Gunicorn {#gunicorn}

[Gunicorn](https://gunicorn.org/) serves as the wsgi server that [nginx](#nginx) proxies to. There is a dedicated systemd unit for managing gunicorn.

### Nginx {#nginx}

[Nginx](https://nginx.org) serves as the web server for serveing static files of the website, and it sends all other requests to [gunicorn]{#gunicorn}. It also has a systemd unit.

There is a [haproxy](https://www.haproxy.org) configuration too. It was tested at an early stage of the project development.

### MySQL {#mysql-and-sqlite}

[MySQL](https://www.mysql.com) and [SQLite](https://sqlite.org) are the databases that are supported. SQLite is used for the demo app and in development for now. MySQL was the original database, but it was swapped for SQLite for its simplicity. 

### Fabric {#fabric}

There are [fabric](https://www.fabfile.org) scripts for automatically setting up the web server in a virtual machine. This could be out of date as the server is now hosted in [`pythonanywhere`](https://www.pythonanywhere.com)

### Hatch {#hatch}

[`Hatch`](https://hatch.pypa.io) is the tool that manages the project's python virtual environments and dependencies. All configurations can be found in the [`pyproject.toml`](./pyproject.toml)
