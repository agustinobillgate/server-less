#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Wgrpdep(Base):
	__tablename__ = 'wgrpdep'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="")
	zknr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('zknr', 0)
		super(Wgrpdep, self).__init__(*args, **kwargs)
