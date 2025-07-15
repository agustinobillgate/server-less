#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_vendor(Base):
	__tablename__ = 'eg_vendor'

	activeflag = sa.Column(sa.Boolean, default=False)
	address = sa.Column(sa.String, default="")
	bezeich = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	contact_person = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	email = sa.Column(sa.String, default="")
	fax = sa.Column(sa.String, default="")
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	phone = sa.Column(sa.String, default="")
	vendor_nr = sa.Column(sa.Integer, default=0)
	website = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', False)
		kwargs.setdefault('address', "")
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('contact_person', "")
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('deci2', 0)
		kwargs.setdefault('email', "")
		kwargs.setdefault('fax', "")
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('logi2', False)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		kwargs.setdefault('phone', "")
		kwargs.setdefault('vendor_nr', 0)
		kwargs.setdefault('website', "")
		super(Eg_vendor, self).__init__(*args, **kwargs)
