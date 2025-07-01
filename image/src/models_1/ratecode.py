#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ratecode(Base):
	__tablename__ = 'ratecode'

	argtnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	ch1preis = sa.Column(sa.Numeric, default=0)
	ch2preis = sa.Column(sa.Numeric, default=0)
	char1 = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""])
	code = sa.Column(sa.String, default="")
	deci1 = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	endperiode = sa.Column(sa.Date, default=None)
	erwachs = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Integer, default=0)
	kind2 = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	marknr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	startperiode = sa.Column(sa.Date, default=None)
	wday = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zipreis = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('argtnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeichnung', "")
		kwargs.setdefault('ch1preis', 0)
		kwargs.setdefault('ch2preis', 0)
		kwargs.setdefault('char1', ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""])
		kwargs.setdefault('code', "")
		kwargs.setdefault('deci1', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('endperiode', None)
		kwargs.setdefault('erwachs', 0)
		kwargs.setdefault('kind1', 0)
		kwargs.setdefault('kind2', 0)
		kwargs.setdefault('logi1', [False,False,False,False,False,False,False,False,False])
		kwargs.setdefault('marknr', 0)
		kwargs.setdefault('num1', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('startperiode', None)
		kwargs.setdefault('wday', 0)
		kwargs.setdefault('zikatnr', 0)
		kwargs.setdefault('zipreis', 0)
		super(Ratecode, self).__init__(*args, **kwargs)
