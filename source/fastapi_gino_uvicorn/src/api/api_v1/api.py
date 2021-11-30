from fastapi import APIRouter


from .endpoints import dialogs, users, pages, ws

pagesRouter = APIRouter()
usersRouter = APIRouter()
cloudsRouter = APIRouter()
wsRouter = APIRouter()
dialogsRouter = APIRouter()
dialogsRouter.include_router(router=dialogs.router,prefix="/dialogs")
cloudsRouter.include_router(router=ws.router,prefix="")
pagesRouter.include_router(router=pages.router,prefix="")
usersRouter.include_router(router=users.router,prefix="/users")
