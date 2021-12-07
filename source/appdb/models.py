from uuid import uuid4
from fastapi.param_functions import Cookie
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
        if pass_user is not None:
            pass_user = pass_user.password 
            if pass_user == password:
                return True
            else:
                return False
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
        dialog = await Messages.query.where(Messages.sender_1 == sender_1).gino.first()
        new_message = dialog.message
        new_message = new_message.json()
        new_message.append(messages)
        dialog.update(messages=new_message)
        return new_message


class Cookies(db.Model): 
    __tablename__ = 'cookies'
    value: str =  db.Column(db.String,primary_key=True)
    userId: str = db.Column(db.String, default=0)
   
    date = db.Column(db.DateTime())
    @classmethod
    async def get_or_create(cls,userId,value)-> "Cookies":
        cookie_token = await cls.get(value)
        if cookie_token is None:
            date = datetime.now()
            return await cls.create(value=value,userId=userId,date=date)
        else:
            #print(cookie_token.__dict__)

            datetimes = cookie_token.__dict__
            datetimes = datetimes["__values__"]
            datetimes = datetimes["date"]
            print(datetimes)

            date = datetime.now()
            # date_cookies = cookie_token.date
            # period = date - date_cookies
            # if int(period.days) > 7:
            #     return "Token is no valid"
            # else:
            #     return cls.get(value)
    @classmethod
    async def get_cookie(cls,value) -> "Cookies":
        await Cookies.delete_not_valid_token()
        cookie_token = await cls.get(value)
        if cookie_token is None:
            return 504
        else:
            return cookie_token
    @classmethod
    async def delete_not_valid_token(cls) -> "Cookies":
        cookies = await cls.query.gino.all()
        print(cookies)
        date = datetime.now()
        for i in cookies:
            date_cookies = i.date
            print(date_cookies)
            period = date - date_cookies
            if int(period.days) > 7:
                await cls.delete.where(Cookies.value == i.value).gino.status()
                

class Dopusk_submissions(db.Model): 
    __tablename__ = 'dopusk_submissions'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    student: str =  db.Column(db.String,default='-')
    teacher: str =  db.Column(db.String,default='-')
    subject: str =  db.Column(db.String,default='-')
    status_author: str = db.Column(db.String,default='-')
    status: str =  db.Column(db.String,default='Получено')
 

    @classmethod
    async def get_or_create_dopusk(cls,student,subject,teacher,status_author)-> "Dopusk_submissions":
        dopusk = await cls.query.where(cls.student == student).gino.all()
        if dopusk is not None:
            for i in dopusk:
                dopusk_subject = i.subject
                if dopusk_subject == subject:
                    return i
            return await cls.create(student=student,subject=subject,teacher=teacher,status_author=status_author)
        if dopusk is None:
            return await cls.create(student=student,subject=subject,teacher=teacher,status_author=status_author)

    @classmethod
    async def update_status(cls,student,subject,teacher,new_status,status_author):
        dopusk = await Dopusk_submissions.get_or_create_dopusk(student,subject,teacher,status_author)
        print(dopusk)
        new_dopusk_status = await dopusk.update(status=new_status).apply()
        new_status_author = await dopusk.update(status_author=status_author).apply()
        return 
        
    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()



class Spravka_submissions(db.Model): 
    __tablename__ = 'spravka_submissions'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    student: str =  db.Column(db.String,default='-')
    way_point: str =  db.Column(db.String,default='-')
    status_author: str = db.Column(db.String,default='-')
    quantity: int = db.Column(db.Integer,default=0)
    status: str =  db.Column(db.String,default='Получено')

    @classmethod
    async def get_or_create_spravka(cls,student,way_point,quantity,status_author)-> "Spravka_submissions":
        spravka = await cls.query.where(cls.student == student).gino.all()
        if spravka is not None:
            for i in spravka:
                spravka_way_piont = i.way_point
                if spravka_way_piont == way_point:
                    return i
            return await cls.create(student=student,way_point=way_point,quantity=quantity,status_author=status_author)
        if spravka is None:
            return await cls.create(student=student,way_point=way_point,quantity=quantity,status_author=status_author)

    @classmethod
    async def update_status(cls,student,way_point,quantity,new_status,status_author):
        spravka = await Spravka_submissions.get_or_create_spravka(student,way_point,quantity,status_author)
        print(spravka)
        new_spravka_status = await spravka.update(status=new_status).apply()
        new_status_author = await spravka.update(status_author=status_author).apply()
        return 

    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()    