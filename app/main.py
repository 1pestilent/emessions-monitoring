from fastapi import FastAPI
import uvicorn

from app.models.database import setup_database

app = FastAPI()

@app.get('/setup_database')
async def setup_db():
    return await setup_database()

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 