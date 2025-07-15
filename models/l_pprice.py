#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_pprice(Base):
	__tablename__ = 'l_pprice'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bestelldatum = sa.Column(sa.Date, default=get_current_date())
	betriebsnr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	lief_nr = sa.Column(sa.Integer, default=0)
	warenwert = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('bestelldatum', get_current_date())
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('counter', 0)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('einzelpreis', 0)
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('warenwert', 0)
		super(L_pprice, self).__init__(*args, **kwargs)
