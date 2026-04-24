import requests
import json 
from config import  API_URL

def json_rpc(method, params=None, id=1):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params if params else {},
        "id": id
    }
    try:
        response = requests.post(f"{API_URL}/json_rpc", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in the request: {e}")
        return None

def getinfo():
    try:
        response = requests.get(API_URL + "/getinfo")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_hashrate(hashrate):
    units = ["H/s", "KH/s", "MH/s", "GH/s", "TH/s", "PH/s", "EH/s"]
    index = 0

    while hashrate >= 1000 and index < len(units) - 1:
        hashrate /= 1000
        index += 1

    return f"{hashrate:.2f} {units[index]}"