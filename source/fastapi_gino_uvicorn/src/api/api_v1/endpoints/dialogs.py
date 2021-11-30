from typing import Any, List
from fastapi import APIRouter
from fastapi import Request
from schemas.models import User, UserCreate, UserUpdate, Message,MessageBase
from models.models import User as ORMUser
from models.models import Messages as ORMMessages
from gino import Gino
import os
db = Gino()


router = APIRouter()



@router.post('/', response_model=Message)
async def get_or_create(
    request: Request
) -> Any:
    #dialog : ORMUser = await ORMMessages.get_or_create(**request.dict())
    return 'r'
