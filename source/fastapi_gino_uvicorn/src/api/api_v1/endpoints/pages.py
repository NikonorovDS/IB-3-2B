from typing import Any, List
from fastapi import APIRouter, Request
from schemas.models import User, UserCreate, UserUpdate
from models.models import User as ORMUser 

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="./templates")

