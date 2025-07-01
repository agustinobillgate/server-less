#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Paramtext(Base):
	__tablename__ = 'paramtext'

	betriebsnr = sa.Column(sa.Integer, default=0)
	notes = sa.Column(sa.String, default="")
	number = sa.Column(sa.Integer, default=0)
	passwort = sa.Column(sa.String, default="")
	ptexte = sa.Column(sa.String, default="")
	sprachcode = sa.Column(sa.Integer, default=0)
	txtnr = sa.Column(sa.Integer, default=0)
	wert = sa.Column(sa.Boolean, default=False)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('notes', "")
		kwargs.setdefault('number', 0)
		kwargs.setdefault('passwort', "")
		kwargs.setdefault('ptexte', "")
		kwargs.setdefault('sprachcode', 0)
		kwargs.setdefault('txtnr', 0)
		kwargs.setdefault('wert', False)
		super(Paramtext, self).__init__(*args, **kwargs)
