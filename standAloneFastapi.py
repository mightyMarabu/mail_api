from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from supersecret import pw, log_in

from db_sync import *

class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    content: str

conf = ConnectionConfig(
    MAIL_USERNAME = log_in,
    MAIL_PASSWORD = pw,
    MAIL_FROM = "anyone@outsideofhal.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME = "Dave" ,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    
    #html = """<p>%s</p> """, emailmessage

    message = MessageSchema(
        subject=email.dict().get("subject"),
        recipients=email.dict().get("email"),
        #recipients=['sebastian.schmidt@ot-movimento.de'],
        #body=html,
        body = email.dict().get("content"),
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@app.post("/sendFile")
async def send_attachement(
    background_task: BackgroundTasks,
    mailSubject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File (...),
    email: EmailStr = Form(...),
    sender: str = Form(...)
    ) -> JSONResponse:

    conf = ConnectionConfig(
    MAIL_USERNAME = log_in,
    MAIL_PASSWORD = pw,
    MAIL_FROM = "anyone@outsideofhal.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME = sender + " von Movimento" ,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
    )

    message = MessageSchema(
        subject= mailSubject, #"Rezeptvorschlag",
        recipients=[email],
        #body="Simple background task",
        body=message+"<br><br>Dies ist eine automatisch generierte Email. Bitte antworten Sie an info@ot-movimento.de oder vorname.name@ot-movimento.de Danke.",
        subtype=MessageType.html,
        attachments=[file])

    fm = FastMail(conf)

    background_task.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "done"})

@app.get("/db_sync")
async def sync():
    try:
        syncDB()
        return JSONResponse(status_code=200, content={"message": "Everything went fine. Praise your developers for the good work they're doing almost ervery day ;-)"})
    except:
        return JSONResponse(status_code=500, content={"message": "oh shit! lay back, get a coffee and inform Sebastian.. this may take a while."})
        
