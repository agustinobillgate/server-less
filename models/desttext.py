#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Desttext(Base):
	__tablename__ = 'desttext'

	dtext = sa.Column(sa.String, default="")
	lang = sa.Column(sa.Integer, default=0)
	refcode = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('dtext', "")
		kwargs.setdefault('lang', 0)
		kwargs.setdefault('refcode', 0)
		super(Desttext, self).__init__(*args, **kwargs)
