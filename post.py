# send post request
import requests

url ='http://127.0.0.1:8000/uploadfile/'
#files = {'file': open('docs/sly.pdf', 'rb')}
files={}
r = requests.post(url, files=files)
print (r)