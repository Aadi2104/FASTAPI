from sqlalchemy import Column,Integer,String
from database import Base,engine


class User(Base):
    __tablename__ = "users"
    name = Column(String, unique=True, index=True)
    id= Column(Integer,primary_key=True,index = True) 
    age=Column(Integer)
    email = Column(String, unique=True, index=True)