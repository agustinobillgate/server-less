from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sms_group(Base):
	__tablename__ = 'sms_group'

	activeflag = sa.Column(sa.Boolean, default=False)
	bemerk = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	fdate = sa.Column(sa.Date, default=None)
	grpname = sa.Column(sa.String, default="")
	grpnr = sa.Column(sa.Integer, default=0)
	id = sa.Column(sa.String, default="")
	key = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	tdate = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
