#!/bin/sh
set -e
cd $HOME/emailer
/usr/local/bin/docker-compose run emailer
