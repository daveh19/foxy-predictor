#!/bin/bash

cd /home/ds/notebooks/Python_Gui
PATH=/opt/ds/bin:/usr/bin:/bin:/sbin; export PATH
#echo D no y y y y y y y y y y y | python fox_gui.py 2> /var/log/$(date +%Y-%m-%d_%H:%M).log
#cat cron_input_bayes | python /home/ds/notebooks/Python_Gui/fox_gui.py | sed -e "s/^/$(date -R) /" 2> /tmp/BayesModel.log
date >> /tmp/BayesModel.log
#cat cron_input_bayes | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/BayesModel.log
#cat cron_input_bayes | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/BayesModel.log
#cp Dashboard.html ../html/`date +\%Y\%m\%d`-BayesModel.html
#rm Dashboard.html
#cat cron_input_gpflow | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/GPFlowModel.log
#cp Dashboard.html ../html/`date +\%Y\%m\%d`-GPFlowModel.html
#rm Dashboard.html
date >> /tmp/DecayModel.log
cat cron_input_decay | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/DecayModel.log
cp Dashboard.html ../html/Decay/`date +\%Y\%m\%d`-DecayModel.html
rm Dashboard.html
date >> /tmp/LatestModel.log
cat cron_input_latest | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/LatestModel.log
cp Dashboard.html ../html/Latest/`date +\%Y\%m\%d`-LatestModel.html
rm Dashboard.html
date >> /tmp/GPModel.log
cat cron_input_gpflow | python /home/ds/notebooks/Python_Gui/fox_gui.py 2> /tmp/GPModel.log
cp Dashboard.html ../html/GP/`date +\%Y\%m\%d`-GPModel.html
rm Dashboard.html

FILE=$(find ~/notebooks/html -name *LatestModel.html | sort -n | tail -1)
cp -f $FILE ~/notebooks/html/Latest/latest.html;
FILE=$(find ~/notebooks/html -name *DecayModel.html | sort -n | tail -1)
cp -f $FILE ~/notebooks/html/Decay/latest.html;
FILE=$(find ~/notebooks/html -name *GPModel.html | sort -n | tail -1)
cp -f $FILE ~/notebooks/html/GP/latest.html;

exit 0
