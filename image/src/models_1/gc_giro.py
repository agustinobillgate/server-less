#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gc_giro(Base):
	__tablename__ = 'gc_giro'

	bankname = sa.Column(sa.String, default="")
	betrag = sa.Column(sa.Numeric, default=0)
	changed = sa.Column(sa.Date, default=None)
	cid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=get_current_date())
	docu_nr = sa.Column(sa.String, default="")
	duedate = sa.Column(sa.Date, default=None)
	fibukonto = sa.Column(sa.String, default="")
	giro_status = sa.Column(sa.Integer, default=0)
	gironum = sa.Column(sa.String, default="")
	posteddate = sa.Column(sa.Date, default=None)
	res_char = sa.Column(ARRAY(sa.String),default=["","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None])
	res_dec = sa.Column(ARRAY(sa.Numeric),default=[0,0,0])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	res_logi = sa.Column(ARRAY(sa.Boolean),default=[False,False,False])
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bankname', "")
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('changed', None)
		kwargs.setdefault('cid', "")
		kwargs.setdefault('created', get_current_date())
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('duedate', None)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('giro_status', 0)
		kwargs.setdefault('gironum', "")
		kwargs.setdefault('posteddate', None)
		kwargs.setdefault('res_char', ["","",""])
		kwargs.setdefault('res_date', [None,None,None])
		kwargs.setdefault('res_dec', [0,0,0])
		kwargs.setdefault('res_int', [0,0,0])
		kwargs.setdefault('res_logi', [False,False,False])
		kwargs.setdefault('userinit', "")
		super(Gc_giro, self).__init__(*args, **kwargs)
