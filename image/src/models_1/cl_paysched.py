#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_paysched(Base):
	__tablename__ = 'cl_paysched'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.String, default="")
	deci3 = sa.Column(sa.String, default="")
	descript = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	payint = sa.Column(sa.Integer, default=0)
	paynum = sa.Column(sa.Integer, default=0)
	period = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('deci2', "")
		kwargs.setdefault('deci3', "")
		kwargs.setdefault('descript', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', 0)
		kwargs.setdefault('num3', 0)
		kwargs.setdefault('payint', 0)
		kwargs.setdefault('paynum', 0)
		kwargs.setdefault('period', 0)
		super(Cl_paysched, self).__init__(*args, **kwargs)
