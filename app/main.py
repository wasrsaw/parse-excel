import uvicorn
import os

from fastapi import FastAPI
from services import router

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))

app: FastAPI = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)

