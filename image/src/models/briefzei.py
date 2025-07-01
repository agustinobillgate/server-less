#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Briefzei(Base):
	__tablename__ = 'briefzei'

	betriebsnr = sa.Column(sa.Integer, default=0)
	briefnr = sa.Column(sa.Integer, default=0)
	briefzeilnr = sa.Column(sa.Integer, default=0)
	texte = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('briefnr', 0)
		kwargs.setdefault('briefzeilnr', 0)
		kwargs.setdefault('texte', "")
		super(Briefzei, self).__init__(*args, **kwargs)
