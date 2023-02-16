from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from supersecret import pw, log_in

class EmailSchema(BaseModel):
    email: List['sebastian.schmidt@ot-movimento.de']


conf = ConnectionConfig(
    MAIL_USERNAME = log_in,
    MAIL_PASSWORD = pw,
    MAIL_FROM = "deep@space.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Call me Dave9000",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

#app = FastAPI()



