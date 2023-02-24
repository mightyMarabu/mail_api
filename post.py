# send post request

# send post request
import requests

#url = 'http://192.168.3.135:7001/email'
#header={"Content-Type": "application/json; charset=utf-8"}
#data = {"email": ["sebastian.schmidt@ot-movimento.de"], "subject": "test betreff", "content": "test text"}

url = 'http://192.168.3.135:7001/sendFile'
headers={"Content-Type": "multipart/form-data"}
payload = {
    "email": "sebastian.schmidt@ot-movimento.de",
    "message": "Hi there! von hier aus geht's..."
}

file = {'file': open('docs/arnie.pdf', 'rb')}

r = requests.post(url=url, data=payload, files=file)
print (r.text)