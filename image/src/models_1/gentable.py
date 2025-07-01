#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gentable(Base):
	__tablename__ = 'gentable'

	activeflag = sa.Column(sa.Boolean, default=True)
	char_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	combo_ext = sa.Column(ARRAY(sa.String),default=["","",""])
	date_ext = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	deci_ext = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	inte_ext = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	key = sa.Column(sa.String, default="")
	logi_ext = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', True)
		kwargs.setdefault('char_ext', ["","","","","","","","",""])
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('combo_ext', ["","",""])
		kwargs.setdefault('date_ext', [None,None,None,None,None,None,None,None,None])
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('date3', None)
		kwargs.setdefault('deci_ext', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('inte_ext', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('key', "")
		kwargs.setdefault('logi_ext', [False,False,False,False,False,False,False,False,False])
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('logi2', False)
		kwargs.setdefault('logi3', False)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		super(Gentable, self).__init__(*args, **kwargs)
