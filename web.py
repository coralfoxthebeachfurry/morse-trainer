import base64
import io
import os
import tempfile
import wave
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
#Imports the code needed from already made systems(CLI code)
from table import ENCODE_TABLE, DECODE_TABLE
from to_audio import parse_and_synthesize
from from_audio import audio_to_morse

app = FastAPI()
#Allows CORS, but Nginx still gonna block it anyways...
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
SAMPLE_RATE = 44100

def buffer_to_wav_b64(buffer: np.ndarray) -> str:
    pcm = (np.clip(buffer, -1.0, 1.0) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setchannels(1)
        wf.setampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())
    return base64.b64encode(buf.getvalue()).decode()

def text_to_morse(text: str) -> str:
    text = text.strip().lower()
    for ch in text:
        if ch not in ENCODE_TABLE:
            raise ValueError(f"Invalid character: {ch!r}")
    return " ".join(ENCODE_TABLE.get(ch, ch) for ch in text)

def morse_to_text():
    ...
