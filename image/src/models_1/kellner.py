#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kellner(Base):
	__tablename__ = 'kellner'

	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	ignore_pers = sa.Column(sa.Boolean, default=False)
	kcredit_nr = sa.Column(sa.Integer, default=0)
	kel_unique = sa.Column(sa.Boolean, default=False)
	kellner_nr = sa.Column(sa.Integer, default=1)
	kellnername = sa.Column(sa.String, default="")
	kumsatz_nr = sa.Column(sa.Integer, default=0)
	kzahl_nr = sa.Column(sa.Integer, default=0)
	masterkey = sa.Column(sa.Boolean, default=False)
	nullbon = sa.Column(sa.Boolean, default=False)
	saldo = sa.Column(sa.Numeric, default=0)
	sprachcode = sa.Column(sa.Integer, default=1)
	storno_begruendung = sa.Column(sa.Boolean, default=False)
	updatedatum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('ignore_pers', False)
		kwargs.setdefault('kcredit_nr', 0)
		kwargs.setdefault('kel_unique', False)
		kwargs.setdefault('kellner_nr', 1)
		kwargs.setdefault('kellnername', "")
		kwargs.setdefault('kumsatz_nr', 0)
		kwargs.setdefault('kzahl_nr', 0)
		kwargs.setdefault('masterkey', False)
		kwargs.setdefault('nullbon', False)
		kwargs.setdefault('saldo', 0)
		kwargs.setdefault('sprachcode', 1)
		kwargs.setdefault('storno_begruendung', False)
		kwargs.setdefault('updatedatum', None)
		super(Kellner, self).__init__(*args, **kwargs)
