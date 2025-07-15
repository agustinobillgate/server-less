#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Rmbudget(Base):
	__tablename__ = 'rmbudget'

	currency = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	logis = sa.Column(sa.Numeric, default=0)
	res_char = sa.Column(ARRAY(sa.String),default=["","",""])
	res_deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	sysdate = sa.Column(sa.Date, default=get_current_date())
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('currency', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('logis', 0)
		kwargs.setdefault('res_char', ["","",""])
		kwargs.setdefault('res_deci', [0,0,0])
		kwargs.setdefault('res_int', [0,0,0])
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('zeit', 0)
		kwargs.setdefault('zikatnr', 0)
		kwargs.setdefault('zimmeranz', 0)
		super(Rmbudget, self).__init__(*args, **kwargs)
