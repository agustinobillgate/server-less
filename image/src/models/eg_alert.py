from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_alert(Base):
	__tablename__ = 'eg_alert'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	create_by = sa.Column(sa.Integer, default=0)
	create_date = sa.Column(sa.Date, default=None)
	create_time = sa.Column(sa.Integer, default=0)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	fromfile = sa.Column(sa.String, default="")
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	msg = sa.Column(sa.String, default="")
	msgstatus = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	reqnr = sa.Column(sa.Integer, default=0)
	sendnr = sa.Column(sa.String, default="")
	sendto = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
