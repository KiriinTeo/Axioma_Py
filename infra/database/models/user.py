from sqlalchemy import Column, String, Boolean, Integer
#from sqlalchemy.dialects.postgresql import UUID
#from uuid import uuid4
from infra.database.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
