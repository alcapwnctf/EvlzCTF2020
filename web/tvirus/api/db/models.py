import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Float
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    """User information
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    organization = Column(String)
    pass_hash = Column(String)
    is_admin = Column(Boolean, default=False)
    session = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

    vaccines = relationship("Vaccine", backref="user", order_by="desc(Vaccine.created_on)")

class Vaccine(Base):
    """Vaccine created by user. 
    """
    __tablename__ = "vaccine"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, default="")
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    approved = Column(Boolean, default=False)
    approved_on = Column(DateTime)

    user_id = Column(Integer, ForeignKey("user.id")) 
