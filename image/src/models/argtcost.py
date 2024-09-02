from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Argtcost(Base):
	__tablename__ = 'argtcost'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	artnrfront = sa.Column(sa.Integer, default=0)
	costbetrag = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	gastnrmember = sa.Column(sa.Integer, default=0)
	mealcoupon = sa.Column(sa.Integer, default=0)
	nettobetrag = sa.Column(sa.Numeric, default=0)
	res_char = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	res_deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	res_logic = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	shift = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
