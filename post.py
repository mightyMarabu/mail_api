# send post request
import requests

#url ='http://127.0.0.1:8000/files/'
#url ='http://127.0.0.1:8000/filesforms/'
url ='http://127.0.0.1:8000/uploadfile/'
files = {'file': open('docs/sly.pdf', 'rb')}
#files = {}
token = {'email': 'sebastian.schmidt@ot-movimento.de'}
r = requests.post(url, files=files)
print (r)