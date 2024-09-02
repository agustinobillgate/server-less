from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ap_journal(Base):
	__tablename__ = 'ap_journal'

	bemerk = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	lief_nr = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	netto = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	rgdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	userinit = sa.Column(sa.String, default="")
	zahlkonto = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
