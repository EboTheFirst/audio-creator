import random
import shutil
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy.io.wavfile import write
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

print(dict(r="124", t="567"))

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
    dataArray = list(map(float,audio.audio.split(',')))
    mn = min(dataArray)
    mx = max(dataArray)
    prescaled = [((2 *(data - mn))/(mx-mn) - 1) for data in dataArray]
    scaled = np.int16(prescaled/np.max(np.abs(prescaled)) * 32767)

    try:
        write('test.wav', 2000, scaled)
        scaled = list(map(float,scaled))
        response = {
            "audioArray": scaled,
            "size": len(scaled),
            }
    except Exception as e:
        
        response = {
            "msg": "Something went wrong",
            "exception": repr(e)
        }
    

    mp_encoder = MultipartEncoder(
        fields={
            'device': '633432cc1d2cab3bd54ac739',
            'audio': ('test.wav', open('test.wav','rb'), 'audio/wav'),
        }
    )
    
    url='https://upbeat-backend.herokuapp.com/recordings/'
    r = requests.post(
        url,
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={
            'Content-Type': mp_encoder.content_type,
            "x-auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJEZXZpY2Uga2V5IiwiaWF0IjoxNjY0MzcxNzk5fQ.EBYjmRswL9DFw5I1Bq2XxLgxjjZbeg-6N2FrQ1fpevQ"
            }
    )
    
    # values = { "device": "633432cc1d2cab3bd54ac739"  }
    # # files = dict(audio= open('test.wav','rb'), device="633432cc1d2cab3bd54ac739")
    # files = {'audio': open('test.wav','rb')}
    # headers = {
    #     "x-auth-token": "eyJhbGciOiJIUzI1NiJ9.RGV2aWNlIGtleQ.JSzlXJjf6nY2pl4cOMoRUPW0p7fhs3mYpwSrRdfcXTk",
    #     'content-type': 'multipart/form-data'
    #     }
    # r=requests.post(url,files=files,data=values, headers=headers)
    return r.status_code
