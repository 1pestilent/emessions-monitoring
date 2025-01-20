from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return "Hello world!"

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)