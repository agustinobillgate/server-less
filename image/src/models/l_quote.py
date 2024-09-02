from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_quote(Base):
	__tablename__ = 'l_quote'

	activeflag = sa.Column(sa.Boolean, default=True)
	artnr = sa.Column(sa.Integer, default=0)
	chgdate = sa.Column(sa.Date, default=lambda: get_current_date())
	chgid = sa.Column(sa.String, default="")
	chgtime = sa.Column(sa.Integer, default=0)
	createdate = sa.Column(sa.Date, default=lambda: get_current_date())
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
