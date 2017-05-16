import httplib2
import urllib

def addNewParty(name, abbreviation, leader, alliance):
    #Specify parameters
    #create body for post method
    data = {'name': name, 'abbreviation': abbreviation, 'leader': leader, 'alliance': alliance}
    body = urllib.urlencode(data)
    h = httplib2.Http()
    resp, content = h.request("http://localhost:5000/parties/", method="POST", body=body)
