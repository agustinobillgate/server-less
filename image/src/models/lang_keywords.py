
from sqlalchemy import func, create_engine, Column, Integer, String, JSON, DateTime, Text
import sqlalchemy as sa
from models.base import Base

class Lang_keywords(Base):
    __tablename__ = 'lang_keywords'

    id = sa.Column(sa.Integer, primary_key=True)
    counter = sa.Column(sa.Integer)
    country_id = sa.Column(sa.String)
    lang_value = sa.Column(sa.String)
    lang_variable = sa.Column(sa.String)