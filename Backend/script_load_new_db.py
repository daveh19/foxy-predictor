#!/opt/ds/bin/python
import os

#os.system('source /opt/ds/bin/activate')
print('Initial run directory')
os.system('pwd') 

os.chdir('/home/ds/notebooks/Backend')
print('Changed run directory to')
os.system('pwd')


from endpoints import loadPollingData
print('About to load new polling data from web')
loadPollingData()
print('Automated script to load new polling data ended')

