from sqlalchemy import Column, Integer, Float, Date
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, index=True)
    approved_date = Column(Date, nullable=True)
    denied_date = Column(Date, nullable=True)
    credit_limit = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    loan_term = Column(Integer, nullable=False)
