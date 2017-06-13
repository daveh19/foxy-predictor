import httplib2
import json
import pandas as pd

def getAllParties():
    # FORMAT: https://localhost:5000/parties/
    h = httplib2.Http()
    url = ('http://localhost:5000/parties/')
    resp, content = h.request(url)
    return pd.from_dict(json_dict)
    assert resp.status == 200
