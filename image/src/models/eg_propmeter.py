from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_propmeter(Base):
	__tablename__ = 'eg_propmeter'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	create_date = sa.Column(sa.Date, default=None)
	create_time = sa.Column(sa.Integer, default=0)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	propertynr = sa.Column(sa.Integer, default=0)
	rec_by = sa.Column(sa.String, default="")
	rec_date = sa.Column(sa.Date, default=None)
	rec_time = sa.Column(sa.Integer, default=0)
	val_hour = sa.Column(sa.Integer, default=0)
	val_meter = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
