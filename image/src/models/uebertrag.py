#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Uebertrag(Base):
	__tablename__ = 'uebertrag'

	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		super(Uebertrag, self).__init__(*args, **kwargs)
