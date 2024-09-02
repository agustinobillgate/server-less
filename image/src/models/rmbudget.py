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
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
