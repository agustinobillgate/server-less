#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Pricegrp(Base):
	__tablename__ = 'pricegrp'

	argtnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	endperiode = sa.Column(sa.Date, default=None)
	kindpreis = sa.Column(ARRAY(sa.Numeric),default=[0,0])
	perspreis = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0])
	rueckdatum = sa.Column(sa.Date, default=None)
	ruecktage = sa.Column(sa.Integer, default=0)
	startperiode = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('argtnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeichnung', "")
		kwargs.setdefault('code', "")
		kwargs.setdefault('endperiode', None)
		kwargs.setdefault('kindpreis', [0,0])
		kwargs.setdefault('perspreis', [0,0,0,0,0,0])
		kwargs.setdefault('rueckdatum', None)
		kwargs.setdefault('ruecktage', 0)
		kwargs.setdefault('startperiode', None)
		super(Pricegrp, self).__init__(*args, **kwargs)
