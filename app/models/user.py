from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # correo
    password_hash = Column(String)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    is_admin = Column(Boolean, default=False)
