#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ba_typ(Base):
	__tablename__ = 'ba_typ'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	typ_id = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeichnung', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('typ_id', 0)
		super(Ba_typ, self).__init__(*args, **kwargs)
