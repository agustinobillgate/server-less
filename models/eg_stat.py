#version: 1.0.0.3

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('assign_to', "")
		kwargs.setdefault('category', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('dept', 0)
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('maintask', 0)
		kwargs.setdefault('other_cost', 0)
		kwargs.setdefault('qty', 0)
		kwargs.setdefault('reserve_char1', "")
		kwargs.setdefault('reserve_char2', "")
		kwargs.setdefault('reserve_char3', "")
		kwargs.setdefault('reserve_date1', None)
		kwargs.setdefault('reserve_deci1', 0)
		kwargs.setdefault('reserve_num1', 0)
		kwargs.setdefault('reserve_num2', 0)
		kwargs.setdefault('reserve_num3', 0)
		kwargs.setdefault('source', 0)
		kwargs.setdefault('sppart_cost', 0)
		kwargs.setdefault('sub_task', "")
		kwargs.setdefault('zinr', "")
		super(Eg_stat, self).__init__(*args, **kwargs)
