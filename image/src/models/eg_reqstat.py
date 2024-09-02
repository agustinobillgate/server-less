from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_reqstat(Base):
	__tablename__ = 'eg_reqstat'

	category = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	closedate = sa.Column(sa.Date, default=None)
	closetime = sa.Column(sa.Integer, default=0)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deptnum = sa.Column(sa.Integer, default=0)
	donedate = sa.Column(sa.Date, default=None)
	donetime = sa.Column(sa.Integer, default=0)
	estfinishdate = sa.Column(sa.Date, default=None)
	estfinishtime = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	object = sa.Column(sa.Integer, default=0)
	objectitem = sa.Column(sa.Integer, default=0)
	objecttask = sa.Column(sa.String, default="")
	opendate = sa.Column(sa.Date, default=None)
	opentime = sa.Column(sa.Integer, default=0)
	pic = sa.Column(sa.Integer, default=0)
	processdate = sa.Column(sa.Date, default=None)
	processtime = sa.Column(sa.Integer, default=0)
	reqfrom = sa.Column(sa.Integer, default=0)
	reqstat = sa.Column(sa.Integer, default=0)
	urgency = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
