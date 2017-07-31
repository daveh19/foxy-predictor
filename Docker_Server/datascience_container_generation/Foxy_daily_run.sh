#!/bin/bash

cd /home/ds/notebooks/Python_Gui
PATH=/opt/ds/bin:/usr/bin:/bin:/sbin; export PATH
#echo D no y y y y y y y y y y y | python fox_gui.py 2> /var/log/$(date +%Y-%m-%d_%H:%M).log
cat input | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/$(date +%Y-%m-%d_%H:%M).log
cp Dashboard.html ../html/`date +\%Y\%m\%d`.html
rm Dashboard.html
exit 0
