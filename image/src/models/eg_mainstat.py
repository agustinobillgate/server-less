from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_mainstat(Base):
	__tablename__ = 'eg_mainstat'

	category = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	donedate = sa.Column(sa.Date, default=None)
	estworkdate = sa.Column(sa.Date, default=None)
	frequency = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	mainstatus = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	object = sa.Column(sa.Integer, default=0)
	objectitem = sa.Column(sa.Integer, default=0)
	pic = sa.Column(sa.Integer, default=0)
	workdate = sa.Column(sa.Date, default=None)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
