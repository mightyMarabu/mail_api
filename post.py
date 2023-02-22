# send post request
import requests

#url = 'http://192.168.3.135:7001/email'
url = 'http://127.0.0.1:8000/email'
headers={"Content-Type": "application/json; charset=utf-8"}
data = {"email": ["sebastian.schmidt@ot-movimento.de"], "subject": "test betreff", "content": "test text"}

r = requests.post(url, json=data ,headers=headers)
print (r.text)