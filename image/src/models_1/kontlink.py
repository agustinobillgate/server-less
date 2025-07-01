#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kontlink(Base):
	__tablename__ = 'kontlink'

	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastkont = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnr_kont = sa.Column(sa.Integer, default=None)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betrieb_gastkont', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('gastnr_kont', None)
		kwargs.setdefault('kontakt_nr', 0)
		kwargs.setdefault('reslinnr', 1)
		kwargs.setdefault('resnr', 0)
		super(Kontlink, self).__init__(*args, **kwargs)
