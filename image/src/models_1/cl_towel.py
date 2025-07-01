#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_towel(Base):
	__tablename__ = 'cl_towel'

	activeflag = sa.Column(sa.Boolean, default=True)
	booked = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	servnr = sa.Column(sa.Integer, default=0)
	towelnum = sa.Column(sa.String, default="")
	toweltype = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', True)
		kwargs.setdefault('booked', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', 0)
		kwargs.setdefault('num3', 0)
		kwargs.setdefault('servnr', 0)
		kwargs.setdefault('towelnum', "")
		kwargs.setdefault('toweltype', 0)
		super(Cl_towel, self).__init__(*args, **kwargs)
