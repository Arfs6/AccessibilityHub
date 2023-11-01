# Deploy  

This directory has scripts and files related to deploying accessibility hub.

The servers_config.json file has a json object with two fields, `servers` and `private_key`. `private_key` is mapped to a string which specifies the path to the private key that will be used to connect to the servers via ssh. `servers` is a list of objects (dictionaries in python) with three fields:  

- `host`: Ip address of the server.  
- `user`: User to connect to via ssh.  
- `type`: Type of server. Optional for web servers but mandatory for load balancer server.

The `fabfile.py` is a fabric script that is used to automate deploying, updating pip dependencies and setting up new servers. run:  
```bash
fab -l
```

To see the list of all available commands.
