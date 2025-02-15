from fastapi import FastAPI
import uvicorn

from app.models.database import setup_database
from app.users import views as users
from app.auth import views as auth


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get('/setup_database')
async def setup_db():
    return await setup_database()

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 