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
    login: str = db.Column(db.String,default='-')
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
        user = await cls.create(email=email,phone=phone,role=role,name=name, 
        admission_year=admission_year, course=course,direction=direction,group=group
        ,hostel=hostel,password=str(hash_password.hexdigest()))
    @classmethod
    async def check_password(cls,email,password)-> "User":
        pass_user = await User.query.where(User.email==email).gino.first()
        pass_user = pass_user.password 
        if pass_user == password:
            return True
        else:
            return False
        
class Messages(db.Model): 
    __tablename__ = 'messages'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    sender_1: int =  db.Column(db.Integer,default='-')
    sender_2: int =  db.Column(db.Integer,default='-')
    dialog: db.Column(JSON, nullable=False, server_default="{}")
    
    @classmethod
    async def get_or_create(cls,sender_1,sender_2)-> "Messages":
        dialog = await Messages.query.where(Messages.sender_1 == sender_1 and Messages.sender_2==sender_2).gino.first()
        if dialog is None:
            dialog = await cls.create(sender_1=sender_1,sender_2=sender_2)
            return dialog
        return dialog
    @classmethod
    async def up_message(cls,sender_1,sender_2,messages)-> "Messages":
        dialog = await Messages.query.where(Messages.sender_1 == sender_1 and Messages.sender_2==sender_2).gino.first()
        new_message = dialog.message
        new_message = new_message.json()
        new_message.append(messages)
        dialog.update(messages=new_message)
        return new_message


class Cookies(db.Model): 
    __tablename__ = 'cookies'
    userId: int = db.Column(db.Integer, primary_key=True)
    value: int =  db.Column(db.Integer,default='-')
    date = db.Column(db.DateTime())
    @classmethod
    async def get_or_create(cls,userId,value)-> "Cookies":
        cookie_token = cls.get(userId)
        if cookie_token is None:
            date = datetime.now()
            cls.create(userId=userId,value=value,date=date)
        else:
            date = datetime.now()
            date_cookies = cookie_token.date
            period = date - date_cookies
            if period.days > 7:
                return "Token is no valid"
            else:
                return cls.get(userId)