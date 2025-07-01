#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Salestim(Base):
	__tablename__ = 'salestim'

	ber_datum = sa.Column(sa.Date, default=get_current_date())
	ber_zeit = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_jahr = sa.Column(sa.Integer, default=0)
	bis_monat = sa.Column(sa.Integer, default=0)
	von_jahr = sa.Column(sa.Integer, default=0)
	von_monat = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('ber_datum', get_current_date())
		kwargs.setdefault('ber_zeit', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bis_jahr', 0)
		kwargs.setdefault('bis_monat', 0)
		kwargs.setdefault('von_jahr', 0)
		kwargs.setdefault('von_monat', 0)
		super(Salestim, self).__init__(*args, **kwargs)
