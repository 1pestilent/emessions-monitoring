import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import router
from app.core.config import STATIC_DIR

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 