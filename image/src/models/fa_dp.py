from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_dp(Base):
	__tablename__ = 'fa_dp'

	change_by = sa.Column(sa.String, default="")
	change_date = sa.Column(sa.Date, default=None)
	change_time = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	char4 = sa.Column(sa.String, default="")
	char5 = sa.Column(sa.String, default="")
	create_by = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	date4 = sa.Column(sa.Date, default=None)
	date5 = sa.Column(sa.Date, default=None)
	dec1 = sa.Column(sa.Numeric, default=0)
	dec2 = sa.Column(sa.Numeric, default=0)
	dec3 = sa.Column(sa.Numeric, default=0)
	dec4 = sa.Column(sa.Numeric, default=0)
	dec5 = sa.Column(sa.Numeric, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	logi4 = sa.Column(sa.Boolean, default=False)
	logi5 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	number4 = sa.Column(sa.Integer, default=0)
	number5 = sa.Column(sa.Integer, default=0)
	order_nr = sa.Column(sa.String, default="")
	pay_date = sa.Column(sa.Date, default=None)
	pay_time = sa.Column(sa.Integer, default=0)
	pay_type = sa.Column(sa.String, default="")
	po_flag = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
