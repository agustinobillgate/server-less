from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cross_hdr(Base):
	__tablename__ = 'cross_hdr'

	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	date4 = sa.Column(sa.Date, default=None)
	date5 = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	deci4 = sa.Column(sa.Numeric, default=0)
	deci5 = sa.Column(sa.Numeric, default=0)
	int1 = sa.Column(sa.Integer, default=0)
	int2 = sa.Column(sa.Integer, default=0)
	int3 = sa.Column(sa.Integer, default=0)
	int4 = sa.Column(sa.Integer, default=0)
	int5 = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	logi4 = sa.Column(sa.Boolean, default=False)
	logi5 = sa.Column(sa.Boolean, default=False)
	others_tablenm = sa.Column(sa.String, default="")
	variant_db = sa.Column(sa.Integer, default=0)
	vhp_tableid = sa.Column(sa.Integer, default=0)
	vhp_tablenm = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
