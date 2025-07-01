#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Package(Base):
	__tablename__ = 'package'

	beginn = sa.Column(sa.Date, default=get_current_date())
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	buchtage = sa.Column(sa.Integer, default=0)
	ende = sa.Column(sa.Date, default=None)
	fakttage = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('beginn', get_current_date())
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('buchtage', 0)
		kwargs.setdefault('ende', None)
		kwargs.setdefault('fakttage', 0)
		kwargs.setdefault('gastnr', None)
		super(Package, self).__init__(*args, **kwargs)
