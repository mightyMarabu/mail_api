# send post request

import requests
import json

url = 'http://192.168.3.135:7001/email'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "email": [
        "sebastian.schmidt@ot-movimento.de"
    ],
    "subject": "string",
    "content": "test with chatGPT"
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print (response.text)