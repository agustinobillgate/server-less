#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Raum(Base):
	__tablename__ = 'raum'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	groesse = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	sortierfolge = sa.Column(sa.Integer, default=0)
	user_group = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	vorbereit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('groesse', 0)
		kwargs.setdefault('nebenstelle', "")
		kwargs.setdefault('personen', 0)
		kwargs.setdefault('preis', 0)
		kwargs.setdefault('raum', "")
		kwargs.setdefault('sortierfolge', 0)
		kwargs.setdefault('user_group', 0)
		kwargs.setdefault('vname', "")
		kwargs.setdefault('vorbereit', 0)
		super(Raum, self).__init__(*args, **kwargs)
