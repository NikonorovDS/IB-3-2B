from typing import Any, List
from fastapi import APIRouter
from fastapi import Request
from schemas.models import User, UserCreate, UserUpdate, UserLogin
from models.models import User as ORMUser
from models.models import Cookies as ORMCookies 
from gino import Gino
import os
db = Gino()
from uuid import uuid4


router = APIRouter()

@router.get('/', response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
        Retrieve users.
    """
    users = await ORMUser.query.gino.all()
    return users

@router.post('/login')
async def login(request : UserLogin,response = Request) -> Any: 
    check : ORMUser = await ORMUser.check_password(**request.dict())
    username = request.dict()
    username = username["email"]
    if check is True:
        value = str(uuid4()).replace('-', '')
        response = {"message":"Yesssss"}
        add_cookies : ORMCookies(userId=username,value=value)
        response.set_cookie(key=username,value=value)
        
        return response
    else:
        return {'message':"password is not valid"}
        

    

@router.post('/')
async def create_user(
    request : UserCreate
) -> Any:
    """
    Create user
    """
    print(request.dict())
    new_user : ORMUser = await ORMUser.create_user(**request.dict())
    return 'ok'


@router.get('/{id}', response_model=User)
async def read_user(
    request: Request,
    id: str
) -> Any:
    """
    Retrieve user by id
    """
    request.app.logger.debug(id)
    user : ORMUser = await ORMUser.get(id)
    return User.from_orm(user)


@router.put('/{id}', response_model=User)
async def update_user(
    id: int,
    request: UserUpdate
) -> Any:
    """
    Update user
    """
    user : ORMUser= await ORMUser.get_or_404(id)
    updated_fields : User = User.from_orm(request)
    await user.update(**updated_fields.dict(skip_defaults=True)).apply()
    return User.from_orm(user)