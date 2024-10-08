from sqlalchemy import Column, Integer, Float, Date, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    score = Column(Float, index=True, default=0)
    approved_date = Column(Date, nullable=True)
    denied_date = Column(Date, nullable=True)
    credit_limit = Column(Integer, nullable=True)
    interest_rate = Column(Float, nullable=True, default=0)
    loan_term = Column(Integer, nullable=True)
