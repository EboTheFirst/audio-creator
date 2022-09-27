import random
import shutil
from typing import Union
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy.io.wavfile import write


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
    dataArray = list(map(float,audio.split(',')))
    mn = min(dataArray)
    mx = max(dataArray)
    prescaled = [((2 *(data - mn))/(mx-mn) - 1) for data in dataArray]
    scaled = np.int16(prescaled/np.max(np.abs(prescaled)) * 32767)

    response = {
        "audioArray": scaled,
        "size": len(scaled),
        }
    try:
        write('test.wav', 2000, scaled)
    except:
        response = {
            "msg": "Something went wrong"
        }
    return scaled
