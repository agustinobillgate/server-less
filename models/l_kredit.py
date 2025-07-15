#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_kredit(Base):
	__tablename__ = 'l_kredit'

	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerk = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	lief_nr = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	mwstbetrag = sa.Column(sa.Numeric, default=0)
	name = sa.Column(sa.String, default="")
	netto = sa.Column(sa.Numeric, default=0)
	opart = sa.Column(sa.Integer, default=0)
	rabatt = sa.Column(sa.Numeric, default=0)
	rabattbetrag = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	rgdatum = sa.Column(sa.Date, default=get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	skonto = sa.Column(sa.Numeric, default=0)
	skontobetrag = sa.Column(sa.Numeric, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	zahlkonto = sa.Column(sa.Integer, default=0)
	ziel = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('counter', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('lscheinnr', "")
		kwargs.setdefault('mwstbetrag', 0)
		kwargs.setdefault('name', "")
		kwargs.setdefault('netto', 0)
		kwargs.setdefault('opart', 0)
		kwargs.setdefault('rabatt', 0)
		kwargs.setdefault('rabattbetrag', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('rgdatum', get_current_date())
		kwargs.setdefault('saldo', 0)
		kwargs.setdefault('skonto', 0)
		kwargs.setdefault('skontobetrag', 0)
		kwargs.setdefault('steuercode', 0)
		kwargs.setdefault('zahlkonto', 0)
		kwargs.setdefault('ziel', 0)
		super(L_kredit, self).__init__(*args, **kwargs)
