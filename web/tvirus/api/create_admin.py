#!/usr/bin/env python
import os
from db import get_db, crud, schemas, engine, models

models.Base.metadata.create_all(bind=engine)

ADMIN_USERNAME = os.getenv("ADMINUSERNAME", "RICKASTLEY")
ADMIN_PASSWORD = os.getenv("ADMINPASSWORD", "GIVEYOUUPNEVERGONNA")
ADMIN_ORGANIZATION = os.getenv("ADMINORGANIZATION", "Internet")

user_schema = schemas.UserCreate(
    username = ADMIN_USERNAME,
    password = ADMIN_PASSWORD,
    organization = ADMIN_ORGANIZATION
)

db = next(get_db())
db.query(models.User).delete()
db.query(models.Vaccine).delete()
db.commit()

crud.create_user(db, user_schema, admin=True)
