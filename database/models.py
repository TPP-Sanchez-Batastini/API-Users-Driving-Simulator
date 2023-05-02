
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("user_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    password = Column("password", String(10000), nullable=False)