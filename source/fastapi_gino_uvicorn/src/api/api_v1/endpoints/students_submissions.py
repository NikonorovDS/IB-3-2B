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
async def create_dopusk(student =Form(...), teacher =Form(...), subject = Form(...),status_author : Optional[str] = Form(...)) -> Any:
    submission = await ORMDopusk_submissions.get_or_create_dopusk(student,subject,teacher,status_author)
    return submission

@router.post('/spravka')
async def create_spravka(student = Form(...), way_point = Form(...), quantity = Form(...)) -> Any:
    submission = await ORMSpravka_submissions.get_or_create_spravka(student,way_point,int(quantity),'-')
    return submission.student, submission.way_point, submission.quantity, submission.status

@router.get("/get_dopusk")
async def get():
    pop = await ORMDopusk_submissions.query.gino.all()
    return pop

@router.post('/update__dopusk_status')
async def update_status(student = Form(...), teacher = Form(...), subject = Form(...), new_status = Form(...), status_author = Form(...)) -> Any:
    status = await ORMDopusk_submissions.update_status(student,subject,teacher,new_status,status_author)
    return status

@router.get("/get_spravka")
async def get():
    pop = await ORMSpravka_submissions.query.gino.all()
    return pop

@router.post('/update_spravka_status')
async def update_status(student = Form(...), way_point = Form(...), quantity = Form(...),new_status = Form(...),status_author = Form(...)) -> Any:
    status = await ORMSpravka_submissions.update_status(student,way_point,int(quantity),new_status,status_author)
    return status