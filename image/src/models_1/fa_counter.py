#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_counter(Base):
	__tablename__ = 'fa_counter'

	count_type = sa.Column(sa.Integer, default=0)
	counters = sa.Column(sa.Integer, default=0)
	dd = sa.Column(sa.Integer, default=0)
	docu_type = sa.Column(sa.Integer, default=0)
	mm = sa.Column(sa.Integer, default=0)
	yy = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('count_type', 0)
		kwargs.setdefault('counters', 0)
		kwargs.setdefault('dd', 0)
		kwargs.setdefault('docu_type', 0)
		kwargs.setdefault('mm', 0)
		kwargs.setdefault('yy', 0)
		super(Fa_counter, self).__init__(*args, **kwargs)
