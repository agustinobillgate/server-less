#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_kateg(Base):
	__tablename__ = 'fa_kateg'

	bezeich = sa.Column(sa.String, default="")
	deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0])
	katnr = sa.Column(sa.Integer, default=0)
	methode = sa.Column(sa.Integer, default=0)
	num = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	nutzjahr = sa.Column(sa.Integer, default=0)
	rate = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('deci', [0,0,0])
		kwargs.setdefault('katnr', 0)
		kwargs.setdefault('methode', 0)
		kwargs.setdefault('num', [0,0,0])
		kwargs.setdefault('nutzjahr', 0)
		kwargs.setdefault('rate', 0)
		super(Fa_kateg, self).__init__(*args, **kwargs)
