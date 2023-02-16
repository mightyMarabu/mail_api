from typing import Union

from fastapi import FastAPI, File, Form, UploadFile
import requests
from mail import *
from fastMail import *

app = FastAPI()


### working ###
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
        sendEmail('u',286,'no file','sorry')
        return {"message": "No upload file sent"}
    else:
        print('success!')

        print (file)
        sendEmail('u',286,'there is a file','now do something with '+ file.filename)
        sendAttachementMail('sebastian.schmidt@ot-movimento.de','there is a file','now do something with '+ file.filename, file)
        return {"filename": file.filename}


@app.post("/filesforms/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


### mail routes ###

@app.get("/sendTextMail/{emailfor}/{receiverID}/{Subject}/{message}/")
async def sendTextEmail(emailfor,receiverID,Subject,message):
    sendEmail(emailfor,receiverID,Subject,message)

    
### using fastmail ###

@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        #recipients="sebastian.schmidt@ot-movimento.de",
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
