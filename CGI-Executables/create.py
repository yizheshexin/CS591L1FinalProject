#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
print ('Content-Type: text/html')
print ('')
import cgi,os
import cgitb;cgitb.enable()
from bs4 import BeautifulSoup
from crontab import CronTab
import requests as re
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, func, desc, case, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from Base import Base
from ClassDef import Course
from crontab import CronTab
form=cgi.FieldStorage()
KeySem = form['SemList'].value
if KeySem == '20203':
	ViewSem = "Fall+2019"
if KeySem == '20204':
	ViewSem = "Spring+2020"
college = form['College'].value
department = form['Department'].value
course = form['Course'].value
section = 'a1'#form['Section'].value
email = form['Email'].value
url = ("https://www.bu.edu/link/bin/uiscgi_studentlink.pl"
"/1575776953?ModuleName=univschr.pl"
"&SearchOptionDesc=Class+Number"
"&SearchOptionCd=S"
"&KeySem={}"
"&ViewSem={}"
"&College={}"
"&Dept={}"
"&Course={}"
"&Section=a1").format(KeySem, ViewSem, college, department, course)
response = re.get(url)
content = response.content
soup = BeautifulSoup(content, 'html.parser')
result = soup.body.find_all('table',recursive=False)[3].find_all('tr',recursive=False)[2].find_all('td',recursive=False)[6]
openseat = int(result.string)
ts = time.time()
if openseat == 0:
    engine = create_engine('sqlite:////var/www/html/coursedb')
    Base.metadata.create_all(engine)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    record=Course(Semseter = ViewSem,College = college,Department = department,Course = course,Seat = openseat,Email = email,Time = ts)
    session.add(record)
    session.commit()
    my_cron = CronTab(user=True)
    command = ('python3 /var/www/html/CGI-Executables/webspider.py '
               '{} {} {} {} {} {} >> /var/www/html/CGI-Executables/spider.log').format(KeySem, ViewSem, college, department, course, email)
    job = my_cron.new(command = command)
    job.minute.every(30)
    my_cron.write()
    print ("""\
        <html>
        <head>
        <title>create mission</title>
        </head>
        <body>
        <h1>Dear {}:</h1>
        <h4>your tracking mission has been succefully set up!
        <br>
        You can go back to home page to explore other interesting parts.
        <br></h4>
        <a href="/index2.html">
        <button>Go Back to Home Page</button>
        </a>
        </body>
        </html>
        """.format(email))



if openseat > 0:
    print ("""\
        <html>
        <head>
        <title>create mission</title>
        </head>
        <body>
        <h1>The open seat for this course is > 0, go and select it!</h1>
        <h2>Go------><a href="https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1576106474?applpath=menu.pl&NewMenu=Home">Student Link</a></h2>
        <br>
        <a href="/index2.html">
        <button>Go Back to Home Page</button>
        </a>
        </body>
        </html>
        """)
