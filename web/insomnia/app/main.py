from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from generator import MemeGenerator, MemeNotFoundError

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""API Endpoints """
class MemeDataIn(BaseModel):
    top: str
    bottom: str
    meme: str

@app.post('/api/meme')
async def meme(config: MemeDataIn):
    
    config_yaml = f'''top: {config.top}
bottom: {config.bottom}
meme: {config.meme}
'''
    try:
        meme = MemeGenerator(config_yaml)
        meme.build()
    except MemeNotFoundError:
        raise HTTPException(status_code=400, detail={"error": f'Invalid meme: {config.meme}'})

    return StreamingResponse(meme.image_stream, media_type="image/png")
