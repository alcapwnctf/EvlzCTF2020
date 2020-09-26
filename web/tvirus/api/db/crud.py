import uuid
import hashlib
from typing import List
from sqlalchemy import desc
from dataclasses import dataclass
from sqlalchemy.orm import Session

from . import models, schemas

@dataclass
class UserNotFoundError(Exception):
    user_id: int

def get_user(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).get(user_id)
    if db_user is None:
        raise UserNotFoundError(user_id=user_id)

    return db_user

def get_user_from_session(db: Session, session: str) -> models.User:
    return db.query(models.User).filter_by(session=session).first()
    
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).order_by(desc(models.User.created_on)).offset(skip).limit(limit).all()

class MakeAdminCommitError(Exception):
    pass

def make_admin(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).get(user_id)
    db_user.is_admin = True

    try:
        db.commit()
    except:
        db.rollback()
        raise MakeAdminCommitError()
    
    db.refresh(db_user)
    return db_user

class CreateUserCommitError(Exception):
    pass

def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session() -> str:
    return str(uuid.uuid4())

class InvalidCredentialsError(Exception):
    pass

class LoginUserCommitError(Exception):
    pass

def login_user(db: Session, user: schemas.UserLogin) -> models.User:
    pass_hash = hash_pass(user.password)

    db_user = db.query(models.User).filter_by(username=user.username).first()
    if not db_user:
        raise InvalidCredentialsError()

    if not db_user.pass_hash == pass_hash:
        raise InvalidCredentialsError()

    db_user.session = generate_session()
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise LoginUserCommitError(e)
        
    return db_user

def create_user(db: Session, user: schemas.UserCreate, admin: bool = False) -> models.User:
    pass_hash = hash_pass(user.password)

    db_user = models.User(
        username=user.username,
        organization=user.organization,
        pass_hash=pass_hash,
        is_admin=admin,
        session=generate_session()
    )
    db.add(db_user)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise CreateUserCommitError(e)

    db.refresh(db_user)
    return db_user

class CreateVaccineCommitError(Exception):
    pass

class VaccineAlreadyExistsError(Exception):
    pass

def create_vaccine(db: Session, user_id: int, vaccine: schemas.VaccineCreate, approve: bool = False):
    vaccine_check = db.query(models.Vaccine).filter_by(name=vaccine.name).first()
    if vaccine_check is not None:
        raise VaccineAlreadyExistsError()
    
    db_user = db.query(models.User).get(user_id)

    if db_user is None:
        raise UserNotFoundError(user_id=user_id)
    
    db_vaccine = models.Vaccine(
        name=vaccine.name,
        description=vaccine.description,
        approved=approve,
    )
    
    db.add(db_vaccine)
    db_user.vaccines.append(db_vaccine)

    try:
        db.commit()
    except Exception as e:
        raise CreateVaccineCommitError(e)

    db.refresh(db_vaccine)
    db.refresh(db_user)

    return db_user
