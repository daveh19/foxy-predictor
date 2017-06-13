import json
import pandas as pd

def getAllParties():
    response = pd.read_json('http://localhost:5000/parties/')
    #jsonResponse = json.load(response.decode('utf-8'))
    return response
