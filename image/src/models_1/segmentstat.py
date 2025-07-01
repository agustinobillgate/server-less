#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Segmentstat(Base):
	__tablename__ = 'segmentstat'

	betriebsnr = sa.Column(sa.Integer, default=0)
	budlogis = sa.Column(sa.Numeric, default=0)
	budpersanz = sa.Column(sa.Integer, default=0)
	budzimmeranz = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	gratis = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Integer, default=0)
	kind2 = sa.Column(sa.Integer, default=0)
	logis = sa.Column(sa.Numeric, default=0)
	persanz = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('budlogis', 0)
		kwargs.setdefault('budpersanz', 0)
		kwargs.setdefault('budzimmeranz', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('gratis', 0)
		kwargs.setdefault('kind1', 0)
		kwargs.setdefault('kind2', 0)
		kwargs.setdefault('logis', 0)
		kwargs.setdefault('persanz', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('zimmeranz', 0)
		super(Segmentstat, self).__init__(*args, **kwargs)
