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
from models.models import Dopusk_submissions as ORMDopusk_submissions
from models.models import Spravka_submissions as ORMSpravka_submissions
from datetime import date,datetime


db = Gino()


router = APIRouter()


@router.post('/dopusk')
async def create_dopusk(student =Form(...), teacher =Form(...), subject = Form(...),status_author="-") -> Any:
    submission = await ORMDopusk_submissions.get_or_create_dopusk(student,subject,teacher,status_author)
    response =  RedirectResponse('http://localhost/v1/users/create_dopusk',  status_code=status.HTTP_302_FOUND)
    return response

@router.post('/spravka')
async def create_spravka(student, way_point, quantity) -> Any:
    submission = await ORMSpravka_submissions.get_or_create_spravka(student,way_point,int(quantity),'-')
    response =  RedirectResponse('http://localhost/v1/users/create_spravka',  status_code=status.HTTP_302_FOUND)
    return response

@router.get("/get_dopusk")
async def get():
    pop = await ORMDopusk_submissions.query.gino.all()
    return pop

@router.post('/update__dopusk_status')
async def update_status(student , teacher , subject , new_status , status_author ) -> Any:
    status = await ORMDopusk_submissions.update_status(student,subject,teacher,new_status,status_author)
    return status

@router.get("/get_spravka")
async def get():
    pop = await ORMSpravka_submissions.query.gino.all()
    return pop

@router.post('/update_spravka_status')
async def update_status(student , way_point , quantity ,new_status ,status_author ) -> Any:
    status = await ORMSpravka_submissions.update_status(student,way_point,int(quantity),new_status,status_author)
    return status


@router.get('/get_my_dopusk')
async def get_dopusk(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)) -> Any:
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        user: ORMUser = await ORMUser.get_user_for_email(email = userId)
        user = user.__dict__
        value = user['__values__']
        name = value['name']
        dopusk: ORMDopusk_submissions = await ORMDopusk_submissions.get_dopusk_of_user(student = name)
        return dopusk
@router.get('/get_spravka')
async def get_spravka(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)) -> Any:
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        user: ORMUser = await ORMUser.get_user_for_email(email = userId)
        user = user.__dict__
        value = user['__values__']
        name = value['name']
        spravka: ORMSpravka_submissions = await ORMSpravka_submissions.get_spravka_of_user(student = name)
        return spravka
