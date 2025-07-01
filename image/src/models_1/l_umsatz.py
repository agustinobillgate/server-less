#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_umsatz(Base):
	__tablename__ = 'l_umsatz'

	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	endkum = sa.Column(sa.Integer, default=0)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('endkum', 0)
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('zwkum', 0)
		super(L_umsatz, self).__init__(*args, **kwargs)
