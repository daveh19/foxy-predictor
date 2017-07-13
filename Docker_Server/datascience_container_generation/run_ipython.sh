#!/bin/bash

echo 'Starting nginx webserver, port 80'
sudo nginx

echo 'Run python endpoints.py after loading the docker container, it wont work here'
#echo 'Starting our database backend server, internal host 5000'
#(cd /home/ds/notebooks/Backend && python endpoints.py&)

echo 'Starting jupyter notebook server, port 8888'
/opt/ds/bin/jupyter-notebook --no-browser --port 8888 --ip=0.0.0.0 

