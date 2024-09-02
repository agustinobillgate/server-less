from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_trainer(Base):
	__tablename__ = 'cl_trainer'

	activeflag = sa.Column(sa.Boolean, default=True)
	adresse1 = sa.Column(sa.String, default="")
	adresse2 = sa.Column(sa.String, default="")
	birthdate = sa.Column(sa.Date, default=None)
	certificate = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	city = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.String, default="")
	date3 = sa.Column(sa.String, default="")
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	email = sa.Column(sa.String, default="")
	gender = sa.Column(sa.String, default="M")
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	offdays = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False])
	phone = sa.Column(sa.String, default="")
	salary = sa.Column(sa.Numeric, default=0)
	startdate = sa.Column(sa.Date, default=None)
	zip = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
