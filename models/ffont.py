#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ffont(Base):
	__tablename__ = 'ffont'

	bezeichnung = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	contcode = sa.Column(sa.String, default="")
	emu = sa.Column(sa.String, default="")
	make = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeichnung', "")
		kwargs.setdefault('code', "")
		kwargs.setdefault('contcode', "")
		kwargs.setdefault('emu', "")
		kwargs.setdefault('make', "")
		super(Ffont, self).__init__(*args, **kwargs)
