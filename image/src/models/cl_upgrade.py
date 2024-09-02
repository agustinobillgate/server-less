from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_upgrade(Base):
	__tablename__ = 'cl_upgrade'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	fdate = sa.Column(sa.Date, default=None)
	frtype = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	new_fee = sa.Column(sa.Numeric, default=0)
	new_members = sa.Column(sa.String, default="")
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	old_members = sa.Column(sa.String, default="")
	refund = sa.Column(sa.Numeric, default=0)
	remarks = sa.Column(sa.String, default="")
	tdate = sa.Column(sa.Date, default=None)
	totype = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
