#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_stat(Base):
	__tablename__ = 'cl_stat'

	active1 = sa.Column(sa.Integer, default=0)
	active2 = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	datum1 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	freeze = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	processed = sa.Column(sa.Integer, default=0)
	revenue1 = sa.Column(sa.Numeric, default=0)
	revenue2 = sa.Column(sa.Numeric, default=0)
	revenue3 = sa.Column(sa.Numeric, default=0)
	terminate = sa.Column(sa.Integer, default=0)
	typenr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('active1', 0)
		kwargs.setdefault('active2', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('datum1', None)
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('deci2', 0)
		kwargs.setdefault('freeze', 0)
		kwargs.setdefault('key', 0)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('processed', 0)
		kwargs.setdefault('revenue1', 0)
		kwargs.setdefault('revenue2', 0)
		kwargs.setdefault('revenue3', 0)
		kwargs.setdefault('terminate', 0)
		kwargs.setdefault('typenr', 0)
		super(Cl_stat, self).__init__(*args, **kwargs)
