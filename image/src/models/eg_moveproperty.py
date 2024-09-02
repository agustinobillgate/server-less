from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_moveproperty(Base):
	__tablename__ = 'eg_moveproperty'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	fr_location = sa.Column(sa.Integer, default=0)
	fr_room = sa.Column(sa.String, default="")
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	property_nr = sa.Column(sa.Integer, default=0)
	to_location = sa.Column(sa.Integer, default=0)
	to_room = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
