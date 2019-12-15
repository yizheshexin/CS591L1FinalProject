#!/usr/bin/python3.5
# coding: utf-8
print ('Content-Type: text/html')
print ('')
import cgi,os
import cgitb;cgitb.enable()
import requests as re
import smtplib
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, func, desc, case, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from Base import Base
from ClassDef import Course
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
form=cgi.FieldStorage()
KeySem = form['SemList'].value
college = form['College'].value
department = form['Department'].value
course = form['Course'].value
if KeySem == '20203':
    ViewSem = "Fall+2019"
if KeySem == '20204':
    ViewSem = "Spring+2020"
engine = create_engine('sqlite:////var/www/html/coursedb')
Base.metadata.create_all(engine)

# the function to generate the graph for a course
def save_graph(Course,engine,course,college,department,ViewSem):
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    time=[]
    seats=[]
    fig = plt.figure()
    for i in session.query(Course).filter(Course.Course==course, Course.College == college, Course.Department == department, Course.Semseter == ViewSem ).all():
        time.append(i.Time)
        seats.append(i.Seat)
    fig = plt.figure() #figsize=(4, 5)
    plt.xlabel('time')
    plt.ylabel('open seats')
    plt.plot(time,seats)
    plt.savefig('/var/www/html/CGI-Executables/graph.png')
    
    #plt.show()

save_graph(Course,engine,course,college,department,ViewSem)
print ("""\
    <html>
    <head>
    <title>create mission</title>
    </head>
    <body>
    <h1>Below is the open seat trend for {} {} {} {}:<h1>
    <img src='/CGI-Executables/graph.png'  alt="upload picture" />
    <br>
    <a href="/index2.html">
    <button>Home Page</button>
    </a>
    </body>
    </html>
    """.format(ViewSem,college,department,course))




