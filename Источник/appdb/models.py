from uuid import uuid4
#from pydantic.errors import NoneIsAllowedError
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime,timezone
from gino import Gino
import os 
db = Gino()
import hashlib

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# some_engine = create_engine('postgresql://scott:tiger@localhost/')

try:
    from main import db
except:
    import sys
    sys.path.insert(1, '../')
    from database import db
class User(db.Model) :
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True ,autoincrement=True) 
    email: str = db.Column(db.String,default='-')
    phone: str = db.Column(db.String,default='-')
    role: str = db.Column(db.String,default='-')
    name: str = db.Column(db.String,default='-')
    admission_year:str = db.Column(db.String,default='-')
    course: int = db.Column(db.Integer,default='-')
    direction: str = db.Column(db.String,default='-')
    group: str = db.Column(db.String,default='-')
    hostel: str = db.Column(db.String,default='-')
    password: str = db.Column(db.String,default='-')
    @classmethod
    async def create_user(cls,email,phone,role,name, admission_year, course,direction,group,hostel,password) -> "User":
        hash_password = hashlib.sha256(password.encode())
        user = await cls.create(email=email,phone=phone,role=role,name=name, admission_year=admission_year, course=course,direction=direction,group=group
        ,hostel=hostel,password=str(hash_password.hexdigest()))
        


