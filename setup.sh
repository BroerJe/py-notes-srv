#!/bin/bash

#
#  Check Root Priv
#
if [ $(id -u) -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

#
#  Set defaults if not found
#
if [ -z $CONTAINER_NAME ]; then 
    CONTAINER_NAME=py-notes-srv
fi

#
#  Run
#
chdir "$(cd -- "$(dirname "$0")" >/dev/null 2>&1; pwd -P)"
docker build --progress=plain -t $CONTAINER_NAME .