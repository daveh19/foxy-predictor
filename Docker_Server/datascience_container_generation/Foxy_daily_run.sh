#!/bin/bash

cd /home/ds/notebooks/Python_Gui
PATH=/opt/ds/bin:/usr/bin:/bin:/sbin; export PATH
#echo D no y y y y y y y y y y y | python fox_gui.py 2> /var/log/$(date +%Y-%m-%d_%H:%M).log
cat cron_input_bayes | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/$(date +%Y-%m-%d_%H:%M)-BayesModel.log
cp Dashboard.html ../html/`date +\%Y\%m\%d`.html
rm Dashboard.html
cat cron_input_gpflow | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/$(date +%Y-%m-%d_%H:%M)-GPFlowModel.log
cp Dashboard.html ../html/`date +\%Y\%m\%d`.html
rm Dashboard.html
cat cron_input_decay | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/$(date +%Y-%m-%d_%H:%M)-DecayModel.log
cp Dashboard.html ../html/`date +\%Y\%m\%d`.html
rm Dashboard.html
exit 0
