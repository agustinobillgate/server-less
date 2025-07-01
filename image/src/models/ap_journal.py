#version: 1.0.0.3

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
	rgdatum = sa.Column(sa.Date, default=get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	sysdate = sa.Column(sa.Date, default=get_current_date())
	userinit = sa.Column(sa.String, default="")
	zahlkonto = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('lscheinnr', "")
		kwargs.setdefault('netto', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('rgdatum', get_current_date())
		kwargs.setdefault('saldo', 0)
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('zahlkonto', 0)
		kwargs.setdefault('zeit', 0)
		super(Ap_journal, self).__init__(*args, **kwargs)
