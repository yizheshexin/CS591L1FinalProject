import sqlalchemy, os, csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, func, desc, case, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker
from Base import Base
class Course(Base):
    __tablename__ = 'teams'
    Id = Column(Integer, primary_key=True)
    Semseter = Column(String)
    College = Column(String)
    Department = Column(String)
    Course = Column(String)
    Seat = Column(Integer)
    Email = Column(String)
    Time = Column(String)

    def __repr__(self):
        return "<Seat(Id={}, Semseter={},College = {}, Department = {}, Course = {}, Seat = {}, Email = {}, Time = {})>".format(
            self.Id, self.Semseter, self.College, self.Department, self.Course, self.Seat, self.Email, self.Time)
