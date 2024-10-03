#!/bin/bash

#
#  Check Root Priv
#
if [ $(id -u) -ne 0 ] 
then 
    echo "Please run as root"
    exit 1
fi

#
#  Check argument count
#
if [ "$#" < 1 ]; then
    echo "Missing configuration file path"
    exit 1
fi

if [ "$#" < 2 ]; then
    echo "Missing content directory path"
    exit 1
fi

#
#  Set defaults if not found
#
if [ -z $CONTAINER_NAME ]; then 
    CONTAINER_NAME=py-notes-srv
fi

if [ -z $CONTAINER_HOST ]; then 
    CONTAINER_HOST="127.0.0.1"
fi

if [ -z $CONTAINER_PORT ]; then 
    CONTAINER_PORT=8000
fi

CONTAINER_CONFIGURATION_PATH=/var/py-notes-srv/configuration.json
CONTAINER_CONTENT_PATH=/var/py-notes-srv

#
#  Run
#
docker stop $CONTAINER_NAME
docker remove $CONTAINER_NAME
docker run \
    --name $CONTAINER_NAME \
    -e PY_NOTES_SRV_HOST=$CONTAINER_HOST \
    -e PY_NOTES_SRV_PORT=$CONTAINER_PORT \
    --net=host \
    --rm \
    -v $1:$CONTAINER_CONFIGURATION_PATH \
    -v $2:$CONTAINER_CONTENT_PATH \
    $CONTAINER_NAME