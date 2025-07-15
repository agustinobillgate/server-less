#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fixleist(Base):
	__tablename__ = 'fixleist'

	arrangement = sa.Column(sa.String, default="")
	artnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	dekade = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	lfakt = sa.Column(sa.Date, default=None)
	number = sa.Column(sa.Integer, default=1)
	persons = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	sequenz = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('arrangement', "")
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('dekade', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('lfakt', None)
		kwargs.setdefault('number', 1)
		kwargs.setdefault('persons', 0)
		kwargs.setdefault('reslinnr', 1)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('sequenz', 1)
		super(Fixleist, self).__init__(*args, **kwargs)
