#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_locker(Base):
	__tablename__ = 'cl_locker'

	card_num = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	from_date = sa.Column(sa.Date, default=get_current_date())
	from_time = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.Integer, default=0)
	locknum = sa.Column(sa.String, default="")
	to_date = sa.Column(sa.Date, default=get_current_date())
	to_time = sa.Column(sa.Integer, default=0)
	towel = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	towel_in = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	towel_out = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	userinit = sa.Column(sa.String, default="")
	valid_flag = sa.Column(sa.Boolean, default=True)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('card_num', "")
		kwargs.setdefault('codenum', "")
		kwargs.setdefault('from_date', get_current_date())
		kwargs.setdefault('from_time', 0)
		kwargs.setdefault('location', 0)
		kwargs.setdefault('locknum', "")
		kwargs.setdefault('to_date', get_current_date())
		kwargs.setdefault('to_time', 0)
		kwargs.setdefault('towel', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('towel_in', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('towel_out', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('valid_flag', True)
		super(Cl_locker, self).__init__(*args, **kwargs)
