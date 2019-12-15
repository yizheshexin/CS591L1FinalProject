#!/usr/bin/env python
# coding: utf-8

# In[7]:

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

engine = create_engine('sqlite:////var/www/html/coursedb',echo=True)

Base.metadata.create_all(engine)


# the function to get some sample data 
def sample(Course,engine):
    session = sessionmaker(bind=engine)
    s=session()
    t=["0",'20','40','60','80','100','120']
    se=[0,1,3,0,2,5,1]    
    for i in range(len(t)):
        record=Course(**{'Semseter':"Fall+2019",
                       'College':"CAS",
                       'Department':"cs",
                       'Course':'599',
                       'Seat':se[i],
                       'Email':"yuwan@bu.edu",
                       'Time' : t[i]
            })
       # print(record)
        s.add(record)
    record=Course(**{'Semseter':"2019fall",
                       'College':"cas",
                       'Department':"cs",
                       'Course':'599',
                       'Course':2,
                       'Email':"wwssxxyyww@163.com",
                       'Time' : "140"
            })
    s.add(record)
    record=Course(**{'Semseter':"2019fall",
                       'College':"ece",
                       'Department':"cs",
                       'Course':'591L1',
                       'Course':2,
                       'Email':"wwssxxyyww@163.com",
                       'Time' : "160"
            })
    s.add(record)
    s.commit()


    


# In[8]:



sample(Course,engine)


# In[9]:


SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()
print('\n', session.query(Course).all(), '\n')


# In[ ]:





# In[ ]:




