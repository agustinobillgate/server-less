#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_enroll(Base):
	__tablename__ = 'cl_enroll'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	enrolldate = sa.Column(sa.Date, default=get_current_date())
	enrollflag = sa.Column(sa.Boolean, default=False)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	nr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	remarks = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('codenum', "")
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('enrolldate', get_current_date())
		kwargs.setdefault('enrollflag', False)
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('logi2', False)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', 0)
		kwargs.setdefault('remarks', "")
		super(Cl_enroll, self).__init__(*args, **kwargs)
