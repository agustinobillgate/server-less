#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sourccod(Base):
	__tablename__ = 'sourccod'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	source_code = sa.Column(sa.Integer, default=0)
	sourcegrup = sa.Column(sa.Integer, default=1)
	vip_level = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('source_code', 0)
		kwargs.setdefault('sourcegrup', 1)
		kwargs.setdefault('vip_level', 0)
		super(Sourccod, self).__init__(*args, **kwargs)
