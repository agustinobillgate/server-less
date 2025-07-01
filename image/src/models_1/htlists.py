from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ARRAY
from models.base import Base

class Htlists(Base):
    __tablename__ = 'htlists'
    id = Column(Integer, primary_key=True)
    htlcode = Column(String)
    htlip = Column(String)
    htllicense= Column(String)
    htlname = Column(String)
    htlport = Column(String)
    htltoken = Column(String)
    htlurl= Column(String)
    nvisit = Column(Integer)
 

