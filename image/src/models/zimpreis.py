#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zimpreis(Base):
	__tablename__ = 'zimpreis'

	argtnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	endperiode = sa.Column(sa.Date, default=None)
	kindpreis = sa.Column(ARRAY(sa.Numeric),default=[0,0])
	perspreis = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0])
	startperiode = sa.Column(sa.Date, default=None)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('argtnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('endperiode', None)
		kwargs.setdefault('kindpreis', [0,0])
		kwargs.setdefault('perspreis', [0,0,0,0,0,0])
		kwargs.setdefault('startperiode', None)
		kwargs.setdefault('zinr', "")
		super(Zimpreis, self).__init__(*args, **kwargs)
