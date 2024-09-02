from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text
from models.config import Base

class ErrorLog(Base):
    __tablename__ = '_awserror'
    id = Column(Integer, primary_key=True)
    error_message = Column(String)
    traceback_details = Column(Text)
    header_json = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
