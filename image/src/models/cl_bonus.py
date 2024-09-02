from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_bonus(Base):
	__tablename__ = 'cl_bonus'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	datum1 = sa.Column(sa.Date, default=None)
	datum2 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	disc_amt = sa.Column(sa.Numeric, default=0)
	disc_days = sa.Column(sa.Integer, default=0)
	disc_proz = sa.Column(sa.Numeric, default=0)
	exp_date1 = sa.Column(sa.Date, default=None)
	exp_date2 = sa.Column(sa.Date, default=None)
	key = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	memtype = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	remarks = sa.Column(sa.String, default="")
	usrid = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
