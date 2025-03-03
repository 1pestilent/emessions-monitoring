from fastapi import FastAPI
import uvicorn

from app.models.database import setup_database
from app.users import views as users
from app.auth import views as auth
from app.aecs import views as aecs


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(aecs.router)

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 