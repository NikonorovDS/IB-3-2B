from fastapi import APIRouter




from .endpoints import dialogs, users, pages, ws, students_submissions

pagesRouter = APIRouter()
usersRouter = APIRouter()
cloudsRouter = APIRouter()
wsRouter = APIRouter()
dialogsRouter = APIRouter()
submissionsRouter = APIRouter()
cloudsRouter.include_router(router=ws.router,prefix="")
pagesRouter.include_router(router=pages.router,prefix="")
usersRouter.include_router(router=users.router,prefix="/users")
submissionsRouter.include_router(router=students_submissions.router,prefix="/submissions")
dialogsRouter.include_router(router=dialogs.router,prefix="/dialogs")
