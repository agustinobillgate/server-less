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
	created = sa.Column(sa.Date, default=lambda: get_current_date())
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
