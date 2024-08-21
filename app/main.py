import uvicorn
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import router

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))


app: FastAPI = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)

