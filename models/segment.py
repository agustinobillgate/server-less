#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Segment(Base):
	__tablename__ = 'segment'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	segmentcode = sa.Column(sa.Integer, default=0)
	segmentgrup = sa.Column(sa.Integer, default=1)
	vip_level = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('segmentgrup', 1)
		kwargs.setdefault('vip_level', 0)
		super(Segment, self).__init__(*args, **kwargs)
