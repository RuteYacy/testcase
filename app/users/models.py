from sqlalchemy import Column, Integer, Float, Date, String
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    approved_date = Column(Date, nullable=True)
    denied_date = Column(Date, nullable=True)
    credit_limit = Column(Float, nullable=True)
    balance = Column(Float, nullable=True)
