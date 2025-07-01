#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Feiertag(Base):
	__tablename__ = 'feiertag'

	aktiv = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('aktiv', False)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('datum', None)
		super(Feiertag, self).__init__(*args, **kwargs)
