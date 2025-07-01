#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_rezlin(Base):
	__tablename__ = 'h_rezlin'

	artnrlager = sa.Column(sa.Integer, default=0)
	artnrrezept = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	lostfact = sa.Column(sa.Numeric, default=0)
	menge = sa.Column(sa.Numeric, default=0)
	recipe_flag = sa.Column(sa.Boolean, default=False)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnrlager', 0)
		kwargs.setdefault('artnrrezept', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('lostfact', 0)
		kwargs.setdefault('menge', 0)
		kwargs.setdefault('recipe_flag', False)
		super(H_rezlin, self).__init__(*args, **kwargs)
