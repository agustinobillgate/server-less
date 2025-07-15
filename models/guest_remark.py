#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guest_remark(Base):
	__tablename__ = 'guest_remark'

	bemerkung = sa.Column(sa.String, default="")
	chgdate = sa.Column(sa.Date, default=get_current_date())
	chgtime = sa.Column(sa.Integer, default=0)
	cid = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	display_flag = sa.Column(sa.Boolean, default=False)
	gastnr = sa.Column(sa.Integer, default=0)
	res_char = sa.Column(ARRAY(sa.String),default=["","",""])
	res_integer = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	reslinnr = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('chgdate', get_current_date())
		kwargs.setdefault('chgtime', 0)
		kwargs.setdefault('cid', "")
		kwargs.setdefault('codenum', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('display_flag', False)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('res_char', ["","",""])
		kwargs.setdefault('res_integer', [0,0,0])
		kwargs.setdefault('reslinnr', 0)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('zeit', 0)
		super(Guest_remark, self).__init__(*args, **kwargs)
