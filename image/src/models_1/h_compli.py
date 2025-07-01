#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_compli(Base):
	__tablename__ = 'h_compli'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	p_artnr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('epreis', 0)
		kwargs.setdefault('p_artnr', 0)
		kwargs.setdefault('rechnr', 0)
		super(H_compli, self).__init__(*args, **kwargs)
