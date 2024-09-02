from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mc_types(Base):
	__tablename__ = 'mc_types'

	activeflag = sa.Column(sa.Boolean, default=True)
	bemerk = sa.Column(sa.String, default="")
	bev_disc = sa.Column(sa.Numeric, default=0)
	bezeich = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	dauer = sa.Column(sa.Integer, default=0)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	food_disc = sa.Column(sa.Numeric, default=0)
	joinfee = sa.Column(sa.Numeric, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	numstay = sa.Column(sa.Integer, default=0)
	prepaid = sa.Column(sa.Numeric, default=0)
	renewal_fee = sa.Column(sa.Numeric, default=0)
	rm_compli = sa.Column(sa.Integer, default=0)
	rm_disc = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
