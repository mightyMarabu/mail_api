# send post request
import requests

##url ='http://127.0.0.1:8000/files/'
##url ='http://127.0.0.1:8000/filesforms/'
##url ='http://127.0.0.1:8000/uploadfile/'
#url = 'http://127.0.0.1:8000/email'
#files = {'file': open('docs/sly.pdf', 'rb')}
##files = {}
#token = {'email': 'sebastian.schmidt@ot-movimento.de'}
#r = requests.post(url, files=files)
#print (r)


url = 'http://192.168.3.135:7001/email'
mail = {"email": ["sebastian.schmidt@ot-movimento.de"]}
#r = requests.post(url, data=body)
#r = requests.post("http://192.168.3.135:7001/email", data={"email": ["user@example.com","sebastian.schmidt@ot-movimento.de"]})
r = requests.post("http://192.168.3.135:7001/email")
print (r.text)