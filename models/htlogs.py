
from sqlalchemy import func, create_engine, Column, Integer, String, JSON, DateTime, Text
import sqlalchemy as sa
from models.base import Base

class Htlogs(Base):
    __tablename__ = 'htlogs'

    id = sa.Column(sa.Integer, primary_key=True)
    apigateway = sa.Column(sa.String)
    endpoint = sa.Column(sa.String)
    htl_code = sa.Column(sa.String)
    userid = sa.Column(sa.String)
    param1 = sa.Column(sa.String)
    awsreqid = sa.Column(sa.String)
    serverinfo = sa.Column(sa.String)
    useragent = sa.Column(sa.Text)
    loginstatus = sa.Column(sa.Boolean, default=False)
    log = sa.Column(sa.Text)
    ip = sa.Column(sa.String)
    lendata = sa.Column(sa.Integer, default=0)
    groupname = sa.Column(sa.String)
    timestart = sa.Column(sa.DateTime, default=func.now(), server_default=func.now())
    timestamp = sa.Column(sa.DateTime)