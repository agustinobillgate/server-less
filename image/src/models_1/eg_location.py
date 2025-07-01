#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_location(Base):
	__tablename__ = 'eg_location'

	bezeich = sa.Column(sa.String, default="")
	building = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	floor = sa.Column(sa.String, default="")
	guestflag = sa.Column(sa.Boolean, default=False)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('building', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('floor', "")
		kwargs.setdefault('guestflag', False)
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('logi2', False)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		super(Eg_location, self).__init__(*args, **kwargs)
