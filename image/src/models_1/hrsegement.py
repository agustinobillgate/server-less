#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hrsegement(Base):
	__tablename__ = 'hrsegement'

	betriebsnr = sa.Column(sa.Integer, default=0)
	couverts_eff = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	tischanz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('couverts_eff', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('tischanz', 0)
		super(Hrsegement, self).__init__(*args, **kwargs)
