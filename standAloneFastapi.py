from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from supersecret import pw, log_in

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = log_in,
    MAIL_PASSWORD = pw,
    MAIL_FROM = "could_be@anyone.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Call me Dave9000",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()



@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        #recipients=['sebastian.schmidt@ot-movimento.de'],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@app.post("/sendFile")
async def send_file(
    background_task: BackgroundTasks,
    file: UploadFile = File (...),
    email: EmailStr = Form(...)
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        #recipients=['sebastian.schmidt@ot-movimento.de'],
        body=html,
        subtype=MessageType.html,
        attachements=[file])

    fm = FastMail(conf)

    background_task.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "done"})
