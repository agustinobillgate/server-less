#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Counters(Base):
	__tablename__ = 'counters'

	betriebsnr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	counter_bez = sa.Column(sa.String, default="")
	counter_no = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('counter', 0)
		kwargs.setdefault('counter_bez', "")
		kwargs.setdefault('counter_no', 0)
		super(Counters, self).__init__(*args, **kwargs)
