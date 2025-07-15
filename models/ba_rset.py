#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ba_rset(Base):
	__tablename__ = 'ba_rset'

	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	personen = sa.Column(sa.Integer, default=0)
	raum = sa.Column(sa.String, default="")
	segmentcode = sa.Column(sa.Integer, default=0)
	setup_id = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('personen', 0)
		kwargs.setdefault('raum', "")
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('setup_id', 0)
		kwargs.setdefault('vname', "")
		super(Ba_rset, self).__init__(*args, **kwargs)
