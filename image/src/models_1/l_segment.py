#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_segment(Base):
	__tablename__ = 'l_segment'

	betriebsnr = sa.Column(sa.Integer, default=0)
	l_bemerk = sa.Column(sa.String, default="")
	l_bezeich = sa.Column(sa.String, default="")
	l_segmentcode = sa.Column(sa.Integer, default=0)
	l_segmentgrup = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('l_bemerk', "")
		kwargs.setdefault('l_bezeich', "")
		kwargs.setdefault('l_segmentcode', 0)
		kwargs.setdefault('l_segmentgrup', 1)
		super(L_segment, self).__init__(*args, **kwargs)
