from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sms_bcaster(Base):
	__tablename__ = 'sms_bcaster'

	activeflag = sa.Column(sa.Boolean, default=False)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	fdate = sa.Column(sa.Date, default=None)
	id = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	remain = sa.Column(sa.Numeric, default=0)
	sysdate = sa.Column(sa.Date, default=None)
	systime = sa.Column(sa.Integer, default=0)
	tdate = sa.Column(sa.Date, default=None)
	total_point = sa.Column(sa.Numeric, default=0)
	used_point = sa.Column(sa.Numeric, default=0)
	usrnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
