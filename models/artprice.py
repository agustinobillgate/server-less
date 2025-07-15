#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Artprice(Base):
	__tablename__ = 'artprice'

	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	end_time = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	start_time = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('end_time', 0)
		kwargs.setdefault('epreis', 0)
		kwargs.setdefault('start_time', 0)
		super(Artprice, self).__init__(*args, **kwargs)
