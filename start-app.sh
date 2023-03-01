#!/bin/bash

# make sure to edit the cron jobs with the command
# crontab -e
# then add @reboot sh /home/ec2-user/start_app.sh

# start the docker containers
cd /home/ec2-user

# delete previous version of the repository
rm -rf lca-tool

# pull latest update from master branch on github
user=kandersonko
pass=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
domain=github.com
repo=kandersonko/lca-tool
git clone https://${user}:${pass}@${domain}/${repo}

# remove previous containers and volume
cd lca-tool
docker compose down --rmi all
docker volume rm $(docker volume ls -q)

# start the docker containers
docker compose up
