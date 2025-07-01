#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guestbud(Base):
	__tablename__ = 'guestbud'

	argtumsatz = sa.Column(sa.Numeric, default=0)
	bed_nights = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_jahr = sa.Column(sa.Integer, default=0)
	bis_monat = sa.Column(sa.Integer, default=0)
	bis_tag = sa.Column(sa.Integer, default=0)
	f_b_umsatz = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	jahr = sa.Column(sa.Integer, default=0)
	logisumsatz = sa.Column(sa.Numeric, default=0)
	monat = sa.Column(sa.Integer, default=0)
	room_nights = sa.Column(sa.Integer, default=0)
	sonst_umsatz = sa.Column(sa.Numeric, default=0)
	tag = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('argtumsatz', 0)
		kwargs.setdefault('bed_nights', 0)
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bis_jahr', 0)
		kwargs.setdefault('bis_monat', 0)
		kwargs.setdefault('bis_tag', 0)
		kwargs.setdefault('f_b_umsatz', 0)
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('jahr', 0)
		kwargs.setdefault('logisumsatz', 0)
		kwargs.setdefault('monat', 0)
		kwargs.setdefault('room_nights', 0)
		kwargs.setdefault('sonst_umsatz', 0)
		kwargs.setdefault('tag', 0)
		super(Guestbud, self).__init__(*args, **kwargs)
