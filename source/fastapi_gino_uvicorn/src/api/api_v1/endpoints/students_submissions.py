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
from models.models import Student_submissions as ORMStudent_submissions


db = Gino()


router = APIRouter()



@router.get('/gd')
async def get_dopusk() -> Any:
    submission = await ORMStudent_submissions.query.gino.all()
    return submission

@router.get('/gs')
async def get_spravka() -> Any:
    submission = await ORMStudent_submissions.query.gino.all()
    return submission

@router.post('/pd')
async def create_dopusk(student = Form(...), teacher = Form(...), subject = Form(...)) -> Any:
    submission = await ORMStudent_submissions.get_or_create_dopusk(student,subject,teacher)
    return submission

@router.post('/ps')
async def create_spravka(student = Form(...), way_point = Form(...), quantity = Form(...)) -> Any:
    submission = await ORMStudent_submissions.get_or_create_spravka(student,way_point,int(quantity))
    return submission