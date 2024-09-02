from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_queasy(Base):
	__tablename__ = 'eg_queasy'

	att_desc = sa.Column(sa.String, default="")
	attachment = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	hist_fdate = sa.Column(sa.Date, default=None)
	hist_nr = sa.Column(sa.Integer, default=0)
	hist_time = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	price = sa.Column(sa.Numeric, default=0)
	reqnr = sa.Column(sa.Integer, default=0)
	stock_nr = sa.Column(sa.Integer, default=0)
	stock_qty = sa.Column(sa.Integer, default=0)
	usr_nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
