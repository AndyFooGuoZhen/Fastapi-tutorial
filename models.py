# Sqlalchemy (ORM) uses this file to create the database tables

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

#  making a simple blog application

class User(Base):
    __tablename__ = "users"   #Creating a table called users

    id = Column(Integer, primary_key=True, index=True) #Primary key named id
    username = Column(String(50), unique=True) # A String of 50, and its going to be unique


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    userid = Column(Integer)