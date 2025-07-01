#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_bestand(Base):
	__tablename__ = 'l_bestand'

	anf_best_dat = sa.Column(sa.Date, default=get_current_date())
	anz_anf_best = sa.Column(sa.Numeric, default=0)
	anz_ausgang = sa.Column(sa.Numeric, default=0)
	anz_eingang = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	kumrezept = sa.Column(sa.Numeric, default=0)
	lager_nr = sa.Column(sa.Integer, default=0)
	val_anf_best = sa.Column(sa.Numeric, default=0)
	wert_ausgang = sa.Column(sa.Numeric, default=0)
	wert_eingang = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anf_best_dat', get_current_date())
		kwargs.setdefault('anz_anf_best', 0)
		kwargs.setdefault('anz_ausgang', 0)
		kwargs.setdefault('anz_eingang', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('kumrezept', 0)
		kwargs.setdefault('lager_nr', 0)
		kwargs.setdefault('val_anf_best', 0)
		kwargs.setdefault('wert_ausgang', 0)
		kwargs.setdefault('wert_eingang', 0)
		super(L_bestand, self).__init__(*args, **kwargs)
