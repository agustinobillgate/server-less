#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mc_fee(Base):
	__tablename__ = 'mc_fee'

	activeflag = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	artnr2 = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	bez_datum = sa.Column(sa.Date, default=None)
	bez_datum2 = sa.Column(sa.Date, default=None)
	bezahlt = sa.Column(sa.Numeric, default=0)
	bezahlt2 = sa.Column(sa.Numeric, default=0)
	bis_datum = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	usr_init = sa.Column(sa.String, default="")
	usr_init2 = sa.Column(sa.String, default="")
	von_datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('artnr2', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('bez_datum', None)
		kwargs.setdefault('bez_datum2', None)
		kwargs.setdefault('bezahlt', 0)
		kwargs.setdefault('bezahlt2', 0)
		kwargs.setdefault('bis_datum', None)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('key', 0)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('usr_init', "")
		kwargs.setdefault('usr_init2', "")
		kwargs.setdefault('von_datum', None)
		super(Mc_fee, self).__init__(*args, **kwargs)
