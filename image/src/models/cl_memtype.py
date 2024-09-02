from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_memtype(Base):
	__tablename__ = 'cl_memtype'

	activeflag = sa.Column(sa.Boolean, default=True)
	all_flag = sa.Column(sa.Boolean, default=False)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	dauer = sa.Column(sa.Integer, default=0)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	descript = sa.Column(sa.String, default="")
	fdate = sa.Column(sa.Date, default=None)
	fee = sa.Column(sa.Integer, default=0)
	fee1 = sa.Column(sa.Numeric, default=0)
	fee2 = sa.Column(sa.Numeric, default=0)
	fee3 = sa.Column(sa.Numeric, default=0)
	iservice = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	max_adult = sa.Column(sa.Integer, default=1)
	max_children = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.String, default="")
	serviceflag = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False])
	tdate = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
