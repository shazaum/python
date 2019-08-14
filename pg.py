#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import datetime
import smtplib

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def pg(query):
    conn = psycopg2.connect("host=localhost dbname=events user=postgres password=mypasswd")
    db = conn.cursor()
    try:
        db.execute(query)
        result = True
    except psycopg2.Error as e:
        conn.commit()
        result = False

    db.close()
    conn.close()

    return result

def send_mail(send_from, send_to, subject, text, server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


execute = pg("DELETE FROM event WHERE instant < now() - interval '30 days'")
if execute:
    send_mail('shazaum@gmail.com', ['shazaum@gmail.com'], 'My subject', 'deleted.')
else:
    send_mail('shazaum@gmail.com', ['shazaum@gmail.com'], 'My subject', 'Error...')
