#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zwkum(Base):
	__tablename__ = 'zwkum'

	bankett = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="")
	hotelrest = sa.Column(sa.Boolean, default=False)
	mwstsplit = sa.Column(sa.Boolean, default=False)
	steuercod1 = sa.Column(sa.Integer, default=0)
	steuercod2 = sa.Column(sa.Integer, default=0)
	zknr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bankett', False)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('hotelrest', False)
		kwargs.setdefault('mwstsplit', False)
		kwargs.setdefault('steuercod1', 0)
		kwargs.setdefault('steuercod2', 0)
		kwargs.setdefault('zknr', 0)
		super(Zwkum, self).__init__(*args, **kwargs)
