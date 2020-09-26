import os
import json 
import uuid
import base64
import hashlib
import dataclasses
from typing import Optional
from dataclasses import dataclass

from fastapi import FastAPI, Depends, APIRouter, Cookie, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from search import KeyClient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_client = KeyClient()

API_PREFIX = '/api'
V1_TAGS = ['v1']

COOKIE_PREFIX = 'cookie'
USER_PREFIX = 'user'
FUND_PREFIX = 'fund'

SESSID_COOKIE_KEY = 'SESS'

FLAG = os.getenv('FLAG', 'FLAG{FAKE}')

USER_TYPE_ADMIN = 'ADMIN'
USER_TYPE_USER = 'USER'

def verify_session_id(SESS: str = Cookie(None)):
    username, cookie_sessid = SESS.split(':')
    stored_sessid = search_client.get_prefix(COOKIE_PREFIX, username).decode()
    print(stored_sessid)
    if cookie_sessid != stored_sessid:
        raise HTTPException(status_code=403, detail='Session invalid.')

    user_data = search_client.get_prefix(USER_PREFIX, username)
    return deserialize_user(user_data)

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

@dataclass
class User:
    username: str
    password_hash: str
    u_type: str 

def serialize_user(user: User) -> str:
    return json.dumps(user, cls=EnhancedJSONEncoder)
    
def deserialize_user(user_str: str) -> User:    
    return User(**json.loads(user_str))
    

def hash_pass(plain_pass: str) -> str:
    return hashlib.sha256(plain_pass.encode()).hexdigest()

def new_user(username: str, plain_pass: str, u_type: str) -> User:
    hashed_pass = hash_pass(plain_pass)
    return User(
        username=username,
        u_type=u_type,
        password_hash=hashed_pass
    )
    
def new_sessid():
    return str(uuid.uuid4())

"""API V1 Endpoints """
@app.get('/api/list', tags=V1_TAGS)
async def list(user = Depends(verify_session_id)):
    return {
        'types': [
            'fund',
        ]
    }

PAGE_COUNT_LIMIT = 100

@app.get('/api/fetch/{prefix}', tags=V1_TAGS)
async def fetch(prefix: str, query: Optional[str] = '', pg: Optional[int] = 0, count: Optional[int] = Query(10, le=PAGE_COUNT_LIMIT), user = Depends(verify_session_id)):
    keys = search_client.search_prefix(
        prefix, 
        query, 
    )
    total_pages = int(len(keys) / count)
    
    keys = keys[pg*count:pg*count+count]
    
    return {
        'pg': pg,
        'items': [
            item.decode().replace(f'{prefix}:', '')
            for item in keys
        ],
        'last': total_pages
    }

@app.get('/api/fetch/{prefix}/value', tags=V1_TAGS)
async def fetch(prefix: str, query: Optional[str] = '', user = Depends(verify_session_id)):
    val = search_client.get_prefix(
        prefix,  
        query,
    )
    
    return {
        'key': query,
        'value': val,
    }

@app.get('/api/flag', tags=V1_TAGS)
async def flag(SESS: str = Cookie(None), user = Depends(verify_session_id)):
    print(user)
    if user.u_type == USER_TYPE_ADMIN:
        return {
            "detail": FLAG
        }
    raise HTTPException(status_code=400, detail='Nein!')

"""Global Endpoints """
class UserDataIn(BaseModel):
    username: str
    password: str

@app.post('/api/register', tags=V1_TAGS)
async def register(payload: UserDataIn, response: Response):
    username = payload.username
    password = payload.password
    
    u_type = USER_TYPE_USER
    new_user_instance = new_user(username, password, u_type)
    new_user_str = serialize_user(new_user_instance)

    if search_client.get_prefix(USER_PREFIX, username) is not None:
        raise HTTPException(status_code=400, detail='User already exists.')
    
    search_client.write_prefix(
        USER_PREFIX, 
        username, 
        new_user_str
    )

    sessid = new_sessid()
    
    search_client.write_prefix(
        COOKIE_PREFIX,
        new_user_instance.username,
        sessid
    )
    
    response.set_cookie(
        key=SESSID_COOKIE_KEY,
        value=f'{new_user_instance.username}:{sessid}'
    )

    return {
        'success': True
    }

@app.post('/api/login', tags=V1_TAGS)
async def login(payload: UserDataIn, response: Response):
    username = payload.username
    password = payload.password
    
    user_data = search_client.get_prefix(USER_PREFIX, username)
    if user_data is None:
        raise HTTPException(status_code=400, detail='Invalid username')
    user = deserialize_user(user_data)
    if user.password_hash != hash_pass(password):
        raise HTTPException(status_code=400, detail='Invalid password')
    
    sessid = new_sessid()
    
    search_client.write_prefix(
        COOKIE_PREFIX,
        user.username,
        sessid
    )

    response.set_cookie(
        key=SESSID_COOKIE_KEY,
        value=f'{user.username}:{sessid}'
    )

    return {
        'success': True
    }

