import random
import shutil
from typing import Union
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudString(BaseModel):
    audio: str


@app.post("/string")
def test(audio: AudString):
    response = {
        "msg": "Just returning what I got",
        "audio": audio
    }
    return response
