#!/usr/bin/python3.5

import sys
from bs4 import BeautifulSoup
import requests as re
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from Base import Base
from ClassDef import Course
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

KeySem = sys.argv[1]
ViewSem = sys.argv[2]
college = sys.argv[3]
department = sys.argv[4]
course = sys.argv[5]
email = sys.argv[6]
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
engine = create_engine('sqlite:////var/www/html/coursedb')
#engine = create_engine('sqlite:////Users/chuci/apa/coursedb')
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()
record=Course(Semseter = ViewSem,College = college,Department = department,Course = course,Seat = openseat,Email = email,Time = ts)
session.add(record)
session.commit()

my_sender = '' # use your own email service  
my_pass = ''  # use your own email service
my_user = email  

def mail():
    ret = True
    try:
        msg = MIMEText('There is an open seat for {} {} {} {}'.format(ViewSem, college, department, course), 'plain', 'utf-8')
        msg['From'] = formataddr(["cc gmail", my_sender])  
        msg['To'] = formataddr(["reminder email", my_user])  
        msg['Subject'] = "BU course reminder"  

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string()) 
        server.quit()  
    except Exception as e:
        print(e) 
        ret = False
    return ret
if openseat > 0:
    ret = mail()
    if ret:
        print("email is sent successfully | {} {} {} {} {} {}".format(KeySem, ViewSem, college, department, course, email))
    else:
        print("email is failed to be sent | {} {} {} {} {} {}".format(KeySem, ViewSem, college, department, course, email))
else:
    print('No email is sent | {} {} {} {} {} {}'.format(KeySem, ViewSem, college, department, course, email))

