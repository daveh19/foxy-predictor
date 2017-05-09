import httplib2
import urllib

def createANewParty():
name = input('Enter the party name: ')
abbreviation = input('Enter the party abbreviation: ')
leader = input('Enter the party leader: ')
alliance = input('Enter the party alliance: ')

data = {'name': name, 'abbreviation': abbreviation, 'leader': leader, 'alliance': alliance}
body = urllib.urlencode(data)
h = httplib2.Http()
resp, content = h.request("http://localhost:5000/parties/", method="POST", body=body)