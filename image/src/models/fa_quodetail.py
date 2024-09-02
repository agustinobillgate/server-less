from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_quodetail(Base):
	__tablename__ = 'fa_quodetail'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	char4 = sa.Column(sa.String, default="")
	char5 = sa.Column(sa.String, default="")
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
	delivery_date = sa.Column(sa.Date, default=None)
	disc1 = sa.Column(sa.Numeric, default=0)
	disc2 = sa.Column(sa.Numeric, default=0)
	fa_nr = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	logi4 = sa.Column(sa.Boolean, default=False)
	logi5 = sa.Column(sa.Boolean, default=False)
	min_qty = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	number4 = sa.Column(sa.Integer, default=0)
	number5 = sa.Column(sa.Integer, default=0)
	price = sa.Column(sa.Numeric, default=0)
	quotation_nr = sa.Column(sa.String, default="")
	remarks = sa.Column(sa.String, default="")
	time_deliver = sa.Column(sa.Integer, default=0)
	vat = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
