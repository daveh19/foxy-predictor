#! /bin/bash

NAME=$1
FOLDER=$2


CONTAINER=`docker run -d --name "foxy_predictor" -p 8888:8888 -p 80:80 -v $PWD/../../:/home/ds/notebooks dataquestio/python3-starter`
echo $CONTAINER
echo 'Allow  a few seconds for the container to load, then run:'
echo '   docker logs ' $CONTAINER
