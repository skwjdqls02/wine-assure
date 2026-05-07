from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.db.data_base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique=True, index=True, nullable=False)
    password= Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False) #010으로 시작하니 string으로
    real_name = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    