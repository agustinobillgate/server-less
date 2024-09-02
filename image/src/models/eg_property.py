from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_property(Base):
	__tablename__ = 'eg_property'

	activeflag = sa.Column(sa.Boolean, default=True)
	asset = sa.Column(sa.String, default="")
	bezeich = sa.Column(sa.String, default="")
	brand = sa.Column(sa.String, default="")
	capacity = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	dimension = sa.Column(sa.String, default="")
	hourmax = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	maintask = sa.Column(sa.Integer, default=0)
	metermax = sa.Column(sa.Integer, default=0)
	meterrec = sa.Column(sa.Boolean, default=False)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	price = sa.Column(sa.Numeric, default=0)
	spec = sa.Column(sa.String, default="")
	type = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
