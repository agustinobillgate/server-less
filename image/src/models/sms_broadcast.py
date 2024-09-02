from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sms_broadcast(Base):
	__tablename__ = 'sms_broadcast'

	bemerk = sa.Column(sa.String, default="")
	broadcast_msg = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	grpnr = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	mstatus = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	phnumber = sa.Column(sa.String, default="")
	usrid = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
