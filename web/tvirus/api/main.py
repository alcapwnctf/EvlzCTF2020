import os
import json
import datetime
from typing import Optional
from dateutil import parser

from fastapi import FastAPI, HTTPException, Depends, Cookie, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from db import crud, models, schemas, engine, get_db

from helpers import preview
from helpers import cache

FLAG = os.getenv("FLAG", "EVLZ{FAKE_FLAG}FLAG")

models.Base.metadata.create_all(bind=engine)

redis_client = cache.RedisClient()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def client_addr(request: Request):
    return request.client.host

def is_localhost(client_addr: str = Depends(client_addr)):
    if client_addr == 'localhost' or client_addr == '127.0.0.1':
        return True

    return False

def current_user(session: Optional[str] = Cookie(None), db: Session = Depends(get_db), is_localhost: bool = Depends(is_localhost)):
    db_user = crud.get_user_from_session(db, session)
    
    if not db_user and not is_localhost:
        raise HTTPException(status_code=403, detail={"error":"invalid session"}) 
     
    return db_user

def cache_control(request: Request):
    if 'Cache-Control' in request.headers:
        if request.headers['Cache-Control'] == 'no-cache':
            return True
    return False

def cache_fingerprint(request: Request, current_user: models.User = Depends(current_user)) -> str:
    username = "anonymous"
    query_params = ''.join([
        f"{key}{val}"
        for key, val in request.query_params.items()
    ])

    uri = f'{request.method}{request.url.path}{query_params}'
    user_agent = request.headers['User-Agent']
    
    if current_user:
        username = current_user.username

    return cache.cache_fingerprint(username, user_agent, uri) 

def cached_response(cache_fingerprint: str = Depends(cache_fingerprint), cache_control: bool = Depends(cache_control)) -> bytes:
    response = None
    if cache_control:
        redis_client.r.delete(cache_fingerprint)
    else:
        response = redis_client.get(cache_fingerprint)
    
    return response

def cached_response_json(response: Response, cached_response: bytes = Depends(cached_response), cache_fingerprint: str = Depends(cache_fingerprint)) -> bytes:
    data = None
    if cached_response:
        data = json.loads(cached_response)
        data['installed'] = parser.parse(data['installed'])
        if datetime.datetime.utcnow() > data['installed'] + datetime.timedelta(minutes=15):
            redis_client.r.delete(cache_fingerprint)
            return None

        response.headers['Cache-Hit'] = cache_fingerprint
        response.headers['Cache-TTL'] = str(data['installed'] + datetime.timedelta(minutes=15))

    return data

def install_cache_response(key: str, response: dict):
    value = {
        "installed": str(datetime.datetime.utcnow()),
        "response": response
    }
    
    def datetime_handler(x):
        if isinstance(x, datetime.datetime):
            return str(x)
        raise TypeError("Unknown type")
    
    return redis_client.set(key, json.dumps(value, default=datetime_handler))

@app.get("/api/preview")
def get_preview(url: str, cache_control: bool = Depends(cache_control), cached_response_json: dict = Depends(cached_response_json), cache_fingerprint: str = Depends(cache_fingerprint)):
    try:
        if cached_response_json and not cache_control:
            return cached_response_json['response']
        
        url_preview = preview.get_preview(url)
    except preview.InvalidUrlError:
        raise HTTPException(status_code=400, detail={"error": "Invalid URL or cannot fetch URL data."})
    except preview.FailedToGetPreviewError:
        raise HTTPException(status_code=400, detail={"error": "Failed to parse URL data"})

    install_cache_response(cache_fingerprint, url_preview)

    return url_preview

@app.post("/api/user")
def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, user)
        response.set_cookie(key="session", value=user.session)
    except crud.CreateUserCommitError:
        raise HTTPException(status_code=400, detail={"error":"Failed to create user"})

    return schemas.User.from_orm(user)

@app.post("/api/login")
def login_user(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = crud.login_user(db, user)
        response.set_cookie(key="session", value=user.session)
    except crud.InvalidCredentialsError:
        raise HTTPException(status_code=400, detail={"error":"Invalid user credentials!"})

    return schemas.User.from_orm(user)
    
@app.get("/api/user/{user_id}")
def get_user(user_id: int, response: Response, cache_control: bool = Depends(cache_control), cached_response_json: dict = Depends(cached_response_json), cache_fingerprint: str = Depends(cache_fingerprint), is_localhost: bool = Depends(is_localhost), current_user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    try:
        if not is_localhost:
            if current_user.id != user_id:
                raise HTTPException(status_code=403, detail={"error": "nein nein nein, this id not for you!"})

        user = crud.get_user(db, user_id)
    except crud.UserNotFoundError:
        raise HTTPException(status_code=400, detail={"error":"failed to create user"})

    user_schema = schemas.User.from_orm(user)
    user_schema_dict = user_schema.dict()

    install_cache_response(cache_fingerprint, user_schema_dict)

    return user_schema

@app.post("/api/user/{user_id}/vaccine")
def create_vaccine(user_id: int, request: Request, vaccine: schemas.VaccineCreate, is_localhost: bool = Depends(is_localhost), current_user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    try:
        if not is_localhost:
            if current_user.id != user_id:
                raise HTTPException(status_code=403, detail={"error": "nein nein nein, this id not for you!"})

        user_updated = crud.create_vaccine(db, user_id, vaccine)
    except crud.CreateVaccineCommitError:
        raise HTTPException(status_code=400, detail={"error":"Failed to create vaccine"})
    except crud.VaccineAlreadyExistsError:
        raise HTTPException(status_code=400, detail={"error":"Vaccine already exists"})

    user_schema = schemas.User.from_orm(user_updated)
    user_schema_dict = user_schema.dict()

    return user_schema

@app.get("/api/flag")
def get_flag(current_user: models.User = Depends(current_user), cache_control: bool = Depends(cache_control), cached_response_json: dict = Depends(cached_response_json), cache_fingerprint: str = Depends(cache_fingerprint)):
    if cached_response_json and not cache_control:
        return cached_response_json['response']
    
    response = {}
    if current_user:
        if current_user.is_admin:
            response = {
                "flag": FLAG
            }
            install_cache_response(cache_fingerprint, response)
        else:
            raise HTTPException(status_code=403, detail={"error": "you are not admin!"})

    return response
