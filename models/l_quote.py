#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_quote(Base):
	__tablename__ = 'l_quote'

	activeflag = sa.Column(sa.Boolean, default=True)
	artnr = sa.Column(sa.Integer, default=0)
	chgdate = sa.Column(sa.Date, default=get_current_date())
	chgid = sa.Column(sa.String, default="")
	chgtime = sa.Column(sa.Integer, default=0)
	createdate = sa.Column(sa.Date, default=get_current_date())
	createid = sa.Column(sa.String, default="")
	createtime = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	filname = sa.Column(sa.String, default="")
	from_date = sa.Column(sa.Date, default=None)
	lief_nr = sa.Column(sa.Integer, default=0)
	remark = sa.Column(sa.String, default="")
	reserve_char = sa.Column(ARRAY(sa.String),default=["","","","",""])
	reserve_deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0])
	reserve_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0])
	reserve_logic = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False])
	to_date = sa.Column(sa.Date, default=None)
	unitprice = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', True)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('chgdate', get_current_date())
		kwargs.setdefault('chgid', "")
		kwargs.setdefault('chgtime', 0)
		kwargs.setdefault('createdate', get_current_date())
		kwargs.setdefault('createid', "")
		kwargs.setdefault('createtime', 0)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('filname', "")
		kwargs.setdefault('from_date', None)
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('remark', "")
		kwargs.setdefault('reserve_char', ["","","","",""])
		kwargs.setdefault('reserve_deci', [0,0,0,0,0])
		kwargs.setdefault('reserve_int', [0,0,0,0,0])
		kwargs.setdefault('reserve_logic', [False,False,False,False,False])
		kwargs.setdefault('to_date', None)
		kwargs.setdefault('unitprice', 0)
		super(L_quote, self).__init__(*args, **kwargs)
