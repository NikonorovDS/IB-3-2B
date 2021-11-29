from typing import Any, List
from fastapi import APIRouter
from fastapi import Request
from schemas.models import User, UserCreate, UserUpdate
from models.models import User as ORMUser
from gino import Gino
import os
db = Gino()



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