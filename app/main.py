import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router
from app.dashboard import views as dashboard
from app.core.config import STATIC_DIR
from app.core.middleware import AuthMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(router)
app.include_router(dashboard.router)
app.add_middleware(AuthMiddleware)

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True) 