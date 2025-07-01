#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_verbrauch(Base):
	__tablename__ = 'l_verbrauch'

	anz_verbrau = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	wert_verbrau = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anz_verbrau', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('wert_verbrau', 0)
		super(L_verbrauch, self).__init__(*args, **kwargs)
