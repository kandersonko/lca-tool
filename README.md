# lca-tool

## Overview 
The application uses docker compose to orchestrate three containers or services:  a MYSQL database (db), a Flask application (backend) an NGINX proxy to route the request to the backend. The services communicate internally using docker networking and only the proxy is exposed to the internet. When a user sends a request, it is routed from the proxy to the backend.

The application has the following structure:
1. db: contains the database password and Dockerfile
2. backend: contains the Flask application code and Dockerfile
3. proxy: contains the NGINX proxy configuration and Dockerfile

## Development

### Docker
For development, the easiest approach is to use the docker destop application. After installation, any editor can be used to edit the code. However, to spawn a locally development server with the application running, start the docker containers:

```bash
# inside the root folder of the repository, run the command:
docker compose up
```

### Vagrant 
For development with `vagrant`, use `vagrant up` in the root of the repository to build the VM.
Then use `vagrant ssh` to login to the VM. Also, `cd /vagrant` and `./init-database.sh` to initialize the database. Finally, run `docker compose up` to start the containers. 
