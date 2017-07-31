#!/bin/bash
PATH=/opt/ds/bin:/usr/bin:/bin:/sbin; export PATH

echo 'Starting nginx webserver, port 80'
sudo nginx

echo 'Starting endpoints'
cd /home/ds/notebooks/Backend || echo "Cannot CD"
nohup python endpoints.py &
echo 'Finishing endpoints'

echo 'Starting cron'
#cron start
sudo cron

echo 'Adding cron job to ds user'
/usr/bin/crontab -u ds /var/cron.d/Foxy_daily_run

echo 'Starting jupyter notebook server, port 8888'
/opt/ds/bin/jupyter-notebook --no-browser --port 8888 --ip=0.0.0.0
