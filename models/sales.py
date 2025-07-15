#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sales(Base):
	__tablename__ = 'sales'

	argtumsatz = sa.Column(sa.Numeric, default=0)
	bed_nights = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	f_b_umsatz = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	karteityp = sa.Column(sa.Integer, default=0)
	logisumsatz = sa.Column(sa.Numeric, default=0)
	room_nights = sa.Column(sa.Integer, default=0)
	sonst_umsatz = sa.Column(sa.Numeric, default=0)
	sort_nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('argtumsatz', 0)
		kwargs.setdefault('bed_nights', 0)
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('f_b_umsatz', 0)
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('karteityp', 0)
		kwargs.setdefault('logisumsatz', 0)
		kwargs.setdefault('room_nights', 0)
		kwargs.setdefault('sonst_umsatz', 0)
		kwargs.setdefault('sort_nr', 0)
		super(Sales, self).__init__(*args, **kwargs)
