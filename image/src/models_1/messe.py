#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Messe(Base):
	__tablename__ = 'messe'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	mdatum = sa.Column(sa.Date, default=None)
	mtext = sa.Column(sa.String, default="")
	notes = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('mdatum', None)
		kwargs.setdefault('mtext', "")
		kwargs.setdefault('notes', "")
		super(Messe, self).__init__(*args, **kwargs)
