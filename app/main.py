import uvicorn
from fastapi import FastAPI

from app.aecs import views as aecs
from app.aecs.routers import create
from app.auth import views as auth
from app.models.database import setup_database
from app.users import views as users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(aecs.router)
app.include_router(create.router)


if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 