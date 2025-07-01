#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Blinehis(Base):
	__tablename__ = 'blinehis'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	bezeich = sa.Column(sa.String, default="")
	bill_datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	fremdwbetrag = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	sysdate = sa.Column(sa.Date, default=get_current_date())
	userinit = sa.Column(sa.String, default="")
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('bill_datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('epreis', 0)
		kwargs.setdefault('fremdwbetrag', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('waehrungsnr', 0)
		kwargs.setdefault('zeit', 0)
		kwargs.setdefault('zinr', "")
		super(Blinehis, self).__init__(*args, **kwargs)
