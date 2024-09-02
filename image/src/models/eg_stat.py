from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_stat(Base):
	__tablename__ = 'eg_stat'

	assign_to = sa.Column(sa.String, default="")
	category = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	dept = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	maintask = sa.Column(sa.Integer, default=0)
	other_cost = sa.Column(sa.Numeric, default=0)
	qty = sa.Column(sa.Integer, default=0)
	reserve_char1 = sa.Column(sa.String, default="")
	reserve_char2 = sa.Column(sa.String, default="")
	reserve_char3 = sa.Column(sa.String, default="")
	reserve_date1 = sa.Column(sa.Date, default=None)
	reserve_deci1 = sa.Column(sa.Numeric, default=0)
	reserve_num1 = sa.Column(sa.Integer, default=0)
	reserve_num2 = sa.Column(sa.Integer, default=0)
	reserve_num3 = sa.Column(sa.Integer, default=0)
	source = sa.Column(sa.Integer, default=0)
	sppart_cost = sa.Column(sa.Numeric, default=0)
	sub_task = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
