import sys

import psycopg2
from psycopg2.extras import NamedTupleCursor 

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from supersecret import pw

### get Data ###

emailfor = sys.argv[1]
receiverID = sys.argv[2]
#Subject = sys.argv[3]
#message = sys.argv[4]
#pdf = sys.argv[5]

pmail = "select email from patients.patients where p_id = %s" 
umail = "select email from company.mitarbeiter where id = %s"

#pdfname = pdf

def getData(Query,mailid):
    try:
        connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.64', port='5432', password='postgres')
        cur = connect.cursor(cursor_factory = NamedTupleCursor)
        #cur = connect.cursor()
        record_to_insert = (mailid, )
        cur.execute(Query, record_to_insert)
        pg_data = cur.fetchone()
        connect.commit()
        connect.close()
    except:
        print("error")
    else:
        print("data loaded")
        return pg_data.email
    finally:
        print("done")

### Mail script ###



#password = input("Type your password and press enter:")

#port = 485  # For starttls
#smtp_server = "smtp.ionos.de"
#password = 'Mo%22Off365'
#sender_email = "messenger@ot-movimento.de"

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "movimento.messenger@gmail.com"
password = pw


def sendMail(receiver_email,Subject,messageText):
    context = ssl.create_default_context()
    message = """\
Subject:""" + Subject + """

""" + messageText +""" 
This message is sent from your beloved Bot."""
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("email send to "+receiver_email)
        print(message)
    except:
        print("i can't make it..")

### run script ####
    #emailfor = 'u'
    #receiverID = 286
    #Subject = "Post ohne Anhang - Unbedingt ansehen!"
    #message = "testmail"

# if emailfor == 'u':
#     receiver_email = getData(umail,receiverID)
#     receiver = receiver_email.split('.')[0]
#     messageText = "Hi "+receiver+",\n"+message
#     sendMail(receiver_email,Subject,messageText)
# #    print(receiver_email)
# else:
#     receiver_email = getData(pmail,receiverID)
#     receiver = receiver_email.split('.')[0]
#     messageText = "Hi "+receiver+",\n"+message
#     sendMail(receiver_email,Subject,messageText)

#############################################################
def sendAttachementMail(receiver_email,Subject,messageText,attachement):
    context = ssl.create_default_context()
    message = """\
Subject:""" + Subject + """

""" + messageText +""" 
This message is sent from your beloved Bot."""
    
    message.attach(attachement)
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("email send to "+receiver_email)
        print(message)
    except:
        print("i can't make it..")
#############################################################

def sendEmail(emailfor,receiverID,Subject,message):
    if emailfor == 'u':
        receiver_email = getData(umail,receiverID)
        receiver = receiver_email.split('.')[0]
        messageText = "Hi "+receiver+",\n"+message
        sendMail(receiver_email,Subject,messageText)
        return{"email send to":receiver}
    else:
        receiver_email = getData(pmail,receiverID)
        receiver = receiver_email.split('.')[0]
        messageText = "Hi "+receiver+",\n"+message
        sendMail(receiver_email,Subject,messageText)
        return{"email send to":receiver}