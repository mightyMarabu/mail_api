from typing import Union

from fastapi import FastAPI, File, UploadFile

from mail import *

app = FastAPI()


@app.post("/files/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        print('no file sent..!')
        return {"message": "No upload file sent"}
    else:
        print('success!')
        return {"filename": file.filename}

@app.get("/sendAttachement/{emailfor}/{receiverID}/{Subject}/{message}/")
async def sendEmail(emailfor,receiverID,Subject,message):
    if emailfor == 'u':
        receiver_email = getData(umail,receiverID)
        receiver = receiver_email.split('.')[0]
        messageText = "Hi "+receiver+",\n"+message
        sendMail(receiver_email,Subject,messageText)
    #    print(receiver_email)
    else:
        receiver_email = getData(pmail,receiverID)
        receiver = receiver_email.split('.')[0]
        messageText = "Hi "+receiver+",\n"+message
        sendMail(receiver_email,Subject,messageText)
        print('success!')
    