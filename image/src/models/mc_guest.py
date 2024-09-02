from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mc_guest(Base):
	__tablename__ = 'mc_guest'

	activeflag = sa.Column(sa.Boolean, default=False)
	bemerk = sa.Column(sa.String, default="")
	cardnum = sa.Column(sa.String, default="")
	changed = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	created_date = sa.Column(sa.Date, default=None)
	date1 = sa.Column(sa.Date, default=None)
	fdate = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	sales_id = sa.Column(sa.String, default="")
	tdate = sa.Column(sa.Date, default=None)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
