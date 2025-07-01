#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Argtstat(Base):
	__tablename__ = 'argtstat'

	aiflag = sa.Column(sa.Boolean, default=False)
	argtnr = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	gastnrmember = sa.Column(sa.Integer, default=0)
	netto = sa.Column(sa.Numeric, default=0)
	res_char = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	res_deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	res_logic = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('aiflag', False)
		kwargs.setdefault('argtnr', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('gastnrmember', 0)
		kwargs.setdefault('netto', 0)
		kwargs.setdefault('res_char', ["","","","","","","","",""])
		kwargs.setdefault('res_date', [None,None,None,None,None,None,None,None,None])
		kwargs.setdefault('res_deci', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('res_int', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('res_logic', [False,False,False,False,False,False,False,False,False])
		kwargs.setdefault('zinr', "")
		super(Argtstat, self).__init__(*args, **kwargs)
