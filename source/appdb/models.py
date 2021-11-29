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
        
# class User(db.Model):
#     __tablename__ = 'users'

#     id: str = db.Column(db.String(), primary_key=True)  
#     tgId = db.Column(db.Integer(), default=0)
#     vkId = db.Column(db.Integer(), default=0)

#     username: str = db.Column(db.String(), default='-')
#     messages: int = db.Column(db.Integer(), default=0)
#     clouds: int = db.Column(db.Integer(), default=0)

#     @classmethod
#     async def get_or_create(cls,typeId, ids, username) -> "User":
#         id = str(uuid4()).replace('-', '')
#         if typeId == 'tg':  
#             user = await User.query.where(User.tgId == ids).gino.first()
#             if user is None:
#                 return await cls.create(id=str(id),tgId=ids,username=username)
#             return user
#         elif typeId == 'vk':
#             user = await User.query.where(User.vkId == ids).gino.first()
#             if user is None:
#                 return await cls.create(id=id,tgId=ids,username=username)
#             return user
#         else:
#             user = await cls.get(ids)
#             if user is None:
#                 return await cls.create(id=ids,username=username)
#                     user =  await cls.create(tgId=id, username=username)

#         user = await cls.get(id)
        
#             elif typeId == 'vk':
#                 return await cls.create(vkId=id, username=username)
#             else:
#                 return await cls.create(id=id, username=username)
        


#         async def up_messages(self) -> int:
#             """
#             Update the statistics of the messages.    
#             Return the updated value.
#             """
#             await self.update(messages=self.messages+1).apply()
#             return self.messages

#         async def up_clouds(self) -> int:
#             """
#             Update the statistics of the clouds.    
#             Return the updated value.
#             """
#             await self.update(clouds=self.clouds+1).apply()
#             return self.clouds


