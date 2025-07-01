#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Dml_rate(Base):
	__tablename__ = 'dml_rate'

	artnr = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	einzelpreis = sa.Column(sa.Numeric, default=0)
	in_liefunit = sa.Column(sa.Boolean, default=False)
	lief_nr = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('einzelpreis', 0)
		kwargs.setdefault('in_liefunit', False)
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('number1', 0)
		super(Dml_rate, self).__init__(*args, **kwargs)
