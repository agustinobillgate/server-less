from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_histpay(Base):
	__tablename__ = 'cl_histpay'

	amount = sa.Column(sa.Numeric, default=0)
	balance = sa.Column(sa.Numeric, default=0)
	billgastnr = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	datum1 = sa.Column(sa.Date, default=None)
	datum2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	memtype = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	paid = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	remarks = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
