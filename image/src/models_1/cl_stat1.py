#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_stat1(Base):
	__tablename__ = 'cl_stat1'

	anzahl = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	class_nr = sa.Column(sa.Integer, default=0)
	date1 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	key = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('class_nr', 0)
		kwargs.setdefault('date1', None)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('deci2', 0)
		kwargs.setdefault('deci3', 0)
		kwargs.setdefault('key', 0)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		super(Cl_stat1, self).__init__(*args, **kwargs)
