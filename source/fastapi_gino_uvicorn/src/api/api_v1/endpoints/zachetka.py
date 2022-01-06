from typing import Any, List
from fastapi import APIRouter, Request
from schemas.models import User, UserCreate, UserUpdate
from models.models import User as ORMUser
from fastapi import Request,Response,Cookie,Form,FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from models.models import User as ORMUser
from models.models import Cookies as ORMCookies
from models.models import Zachetka as ORMZachetka
from models.models import Notes as ORMNotes
from models.models import Subject as ORMSubject
app = FastAPI()
router = APIRouter()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


@router.get('/start',response_class=HTMLResponse )
async def start(request: Request,response: Response,CookieId: Optional[str] = Cookie(None))-> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    print(check)
    if check == 504:
        response = templates.TemplateResponse('login.html',{"request":request})
        response.delete_cookie("CookieId")
        return response
@router.post('/crateSubcect')
async def createSubject(teacher=Form(...),group=Form(...),subject=Form(...))-> Any:
    create_subject: ORMSubject = await ORMSubject.create_s(teacher,group,subject)
    return create_subject

@router.post('/get_group')
async def get_group(id,CookieId: Optional[str] = Cookie(None)) -> Any:
    request= Request
    response= Response
    get_group: ORMSubject = await ORMSubject.get_students(id=id)
    return get_group
@router.post('/get_subjects')#надо убрать teacher его будем узнавать по кукам 
async def get_subjects(teacher,CookieId: Optional[str] = Cookie(None)) -> Any:
    request= Request
    response= Response
    get_subjects: ORMSubject = await ORMSubject.get_subjects(teacher = teacher)
    return get_subjects
@router.post('/crateNote')
async def create(zachetkaid,teacher,subject,semestr,note)-> Any:
    note : ORMNotes = await ORMNotes.create_note(zachetkaid,teacher,subject,semestr,note)
    return note