#!/bin/bash

docker compose down --rmi all
docker volume rm $(docker volume ls -q)

# start the docker containers
docker compose up
# this is our code.
