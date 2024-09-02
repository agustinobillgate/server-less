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
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	lief_nr = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	mwstbetrag = sa.Column(sa.Numeric, default=0)
	name = sa.Column(sa.String, default="")
	netto = sa.Column(sa.Numeric, default=0)
	opart = sa.Column(sa.Integer, default=0)
	rabatt = sa.Column(sa.Numeric, default=0)
	rabattbetrag = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	rgdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	skonto = sa.Column(sa.Numeric, default=0)
	skontobetrag = sa.Column(sa.Numeric, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	zahlkonto = sa.Column(sa.Integer, default=0)
	ziel = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
