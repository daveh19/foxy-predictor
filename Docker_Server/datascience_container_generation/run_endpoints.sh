#!/bin/bash

PATH=/opt/ds/bin:/usr/bin:/bin:/sbin; export PATH

cd /home/ds/notebooks/Backend || echo "Cannot CD"
nohup python endpoints.py &
