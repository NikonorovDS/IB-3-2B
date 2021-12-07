from typing import Any, List
from fastapi import APIRouter
from fastapi import Request
from schemas.models import User, UserCreate, UserUpdate, Message,MessageBase
from models.models import User as ORMUser
from models.models import Students_submissions as ORMStudents_submissions
from models.models import Cookies as ORMCookies 
from gino import Gino
import os

db = Gino()


router = APIRouter()



@router.get('/sub')
async def get_or_create() -> Any:
    submission = await ORMStudents_submissions.query.gino.all()
    return submission

