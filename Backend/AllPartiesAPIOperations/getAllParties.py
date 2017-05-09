import httplib2
import json

def getAllParties():
    # FORMAT: https://localhost:5000/parties/
    h = httplib2.Http()
    url = ('http://localhost:5000/parties/')
    resp, content = h.request(url)
    assert resp.status == 200

