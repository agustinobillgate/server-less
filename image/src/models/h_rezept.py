#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_rezept(Base):
	__tablename__ = 'h_rezept'

	artnrrezept = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	datumanlage = sa.Column(sa.Date, default=None)
	datummod = sa.Column(sa.Date, default=None)
	kategorie = sa.Column(sa.Integer, default=0)
	portion = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnrrezept', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('datumanlage', None)
		kwargs.setdefault('datummod', None)
		kwargs.setdefault('kategorie', 0)
		kwargs.setdefault('portion', 1)
		super(H_rezept, self).__init__(*args, **kwargs)
