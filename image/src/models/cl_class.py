from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_class(Base):
	__tablename__ = 'cl_class'

	activeflag = sa.Column(sa.Boolean, default=True)
	capacity = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	end_date = sa.Column(sa.Date, default=None)
	end_time = sa.Column(sa.String, default="0000")
	fee1 = sa.Column(sa.Numeric, default=0)
	fee2 = sa.Column(sa.Numeric, default=0)
	instructor = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	location_nr = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	paymode = sa.Column(sa.Integer, default=0)
	start_date = sa.Column(sa.Date, default=None)
	start_time = sa.Column(sa.String, default="0000")
	week_day = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False])
	_recid = sa.Column(sa.Integer, primary_key=True)
