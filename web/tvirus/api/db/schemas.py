import datetime
from typing import List, Optional

from pydantic import BaseModel

class VaccineBase(BaseModel):
    name: str
    description: str

class VaccineCreate(VaccineBase):
    pass

class Vaccine(VaccineBase):
    id: int
    created_on: datetime.datetime
    approved: bool

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserLogin(UserBase):
    password: str

class UserCreate(UserLogin):
    organization: str

class User(UserBase):
    id: int
    organization: str
    is_admin: bool
    created_on: datetime.datetime
    vaccines: List[Vaccine] = []

    class Config:
        orm_mode = True
