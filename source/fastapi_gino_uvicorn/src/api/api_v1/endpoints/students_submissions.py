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


db = Gino()


router = APIRouter()


'''
@router.get('/gd')
async def get_dopusk() -> Any:
    submission = await ORMDopusk_submissions.query.gino.first()#нам нужно реализовать поиск по имени \ преподу , и при этом оставить first(). Чтобы не сломался return
    return submission.student, submission.teacher, submission.subject, submission.status

@router.get('/gs')
async def get_spravka() -> Any:
    submission = await ORMSpravka_submissions.query.gino.first()#нам нужно реализовать поиск по имени \ преподу , и при этом оставить first(). Чтобы не сломался return
    return submission.student, submission.way_point, submission.quantity, submission.status
'''

@router.post('/pd')
async def create_dopusk(student = Form(...), teacher = Form(...), subject = Form(...)) -> Any:
    submission = await ORMDopusk_submissions.get_or_create_dopusk(student,subject,teacher)
    if submission == [] or submission == None:
        pass
    else:
        return submission.student, submission.teacher, submission.subject, submission.status

@router.post('/ps')
async def create_spravka(student = Form(...), way_point = Form(...), quantity = Form(...)) -> Any:
    submission = await ORMSpravka_submissions.get_or_create_spravka(student,way_point,int(quantity))
    return submission.student, submission.way_point, submission.quantity, submission.status
