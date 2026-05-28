import win32com.client as win32
import json
import time
from random import randrange
from pprint import pprint

def send_email(recipients: list, subject: str, message: list, nb_email_to_send: int = 1, email_service: str = "outlook"):

    outlook = win32.Dispatch('outlook.application')

    for i in range(nb_email_to_send):
        mail = outlook.CreateItem(0)
        mail.BodyFormat = 1
        mail.To = ";".join(recipients)

        mail.Subject = subject

        mail.Body = "\n".join(message)
        mail.Send()

        time.sleep(randrange(1, 10))
    