cd /home/ds/notebooks/Python_Gui
echo D no y y y y y y y y y y y | python fox_gui.py 2> /var/log/$(date +%Y-%m-%d_%H:%M).log
cp Dashboard.html ../html/`date +\%Y\%m\%d`.html
rm Dashboard.html
