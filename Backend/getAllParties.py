import httplib2
import json

def getAllParties():
    # FORMAT: https://localhost:5000/parties/
    url = ('http://localhost:5000/parties/')
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    print(result)
    return (result)
