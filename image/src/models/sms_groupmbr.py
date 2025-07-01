#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sms_groupmbr(Base):
	__tablename__ = 'sms_groupmbr'

	activeflag = sa.Column(sa.Boolean, default=False)
	bemerk = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	created_by = sa.Column(sa.String, default="")
	createddate = sa.Column(sa.Date, default=None)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	fdate = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=None)
	grpnr = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	tdate = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', False)
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('created_by', "")
		kwargs.setdefault('createddate', None)
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('fdate', None)
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('grpnr', 0)
		kwargs.setdefault('key', 0)
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('logi2', False)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		kwargs.setdefault('tdate', None)
		super(Sms_groupmbr, self).__init__(*args, **kwargs)
