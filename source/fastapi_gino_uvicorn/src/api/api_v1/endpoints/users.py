import argparse
import sys



from typing import Any, List
from fastapi import APIRouter
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi import Request,Response,Cookie,Form
from typing import Optional
from starlette import responses
import starlette.status as status

from starlette.responses import HTMLResponse
from schemas.models import User, UserCreate, UserUpdate, UserLogin
from models.models import User as ORMUser
from models.models import Cookies as ORMCookies  
from gino import Gino
import os
db = Gino()
from uuid import uuid4
import requests


from fastapi.templating import Jinja2Templates
router = APIRouter()
templates = Jinja2Templates(directory="./templates")
@router.get("/cookies")
async def read_cookies() -> Any:
    cookies = await ORMCookies.query.gino.all()
    return cookies
@router.get("/cookies/delete")
async def delete_cookies()  -> Any:
    return await ORMCookies.delete_not_valid_token()
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
@router.get('/start',response_class=HTMLResponse )
async def start(request: Request,response: Response,CookieId: Optional[str] = Cookie(None))-> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    print(check)
    if check == 504:
        response = templates.TemplateResponse('index.html',{"request":request})
        response.delete_cookie("CookieId")
        return response
    html_content = f"""
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8">
  <title>Форма</title>
 </head>
 <body>
  <form id="auth" action="http://localhost:80/v1/users/login" method="post"></form>
  <p>...</p>
  <p><input name="email" form="auth">
  <input type="password" name="password" form="auth"></p>
  <p><input type="submit" form="auth"></p> 
 </body>
</html>
"""
    return templates.TemplateResponse('index.html',{"request":request})
@router.post('/login')
async def login(email = Form(...),password = Form(...),CookieId: Optional[str] = Cookie(None)) -> Any: 
    #request.json()
    response: Request
    if CookieId is None: 
        check : ORMUser = await ORMUser.check_password(email,password)
        username = email
        if check is True:
            content = {"message": "Come to the dark side, we have cookies"}
            value = str(uuid4()).replace('-', '')
            response = JSONResponse(content=content)
            add_cookies : ORMCookies = await ORMCookies.get_or_create(userId=username,value=value)
            print(add_cookies.__dict__)
            response.set_cookie(key="CookieId", value=value)
            return response
        else:
            return RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    elif CookieId is not None:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        if check == 504:
            return RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        return{'meesage':'Your cookies is True'}
      
        
@router.get('/login_test/{username}')
async def test_login(username: str,password:str ,response: Request)-> Any: 
    check : ORMUser = await ORMUser.check_password(email=username,password=password)
    if check is True:
        value = str(uuid4()).replace('-', '')
        content= 'yess'
        response = JSONResponse(content=content)
        add_cookies : ORMCookies(userId=username,value=value)
        response.set_cookie(key="CookieId",value=value)
        
        return response
    else:
        return requests.get("http://localhost:80/v1/users/start") #{'message':"password is not valid"}
    
@router.get('/test_working')
async def read_cookies(CookieId: Optional[str] = Cookie(None)) -> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    if check == 504:
        return RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    name = check.userId
    return name
   
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


# @router.get('/{id}', response_model=User)
# async def read_user(
#     request: Request,
#     id: str
# ) -> Any:
#     """
#     Retrieve user by id
#     """
#     request.app.logger.debug(id)
#     user : ORMUser = await ORMUser.get(id)
#     return User.from_orm(user)


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