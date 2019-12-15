#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
print ('Content-Type: text/html')
print ('')
import cgi,os
import cgitb;cgitb.enable()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, func, desc, case, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from Base import Base
from ClassDef import Course
form=cgi.FieldStorage()
email = form['Email'].value
engine = create_engine('sqlite:////var/www/html/coursedb')
Base.metadata.create_all(engine)
def get_record_byemail(Course,mail,engine):
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    return session.query(Course).filter(Course.Email==mail).group_by(Course.Semseter, Course.College, Course.Department, Course.Course).all()
result = get_record_byemail(Course, email, engine)
print ("""\
    <html>
    <head>
    <title>create mission</title>
    </head>
    <body>
    <h1>Dear {},</h1>
    Here is all the missions that we create for you:
    <br>
    <table border="1">
    <tr>
        <th>Semseter</th>
        <th>College</th>
        <th>Department</th>
        <th>Course</th>
    </tr>""".format(email))
for each in result:
    Semseter = each.Semseter
    College = each.College
    Department = each.Department
    Course = each.Course
    print("""
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>

        """.format(Semseter, College, Department, Course)
        )
print("""
</table>
    <a href="/index2.html">
    <button>Home Page</button>
    </a>
    </body>
    </html>
    """)
