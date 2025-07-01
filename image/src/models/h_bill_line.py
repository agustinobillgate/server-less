#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_bill_line(Base):
	__tablename__ = 'h_bill_line'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	bill_datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	fremdwbetrag = sa.Column(sa.Numeric, default=0)
	kellner_nr = sa.Column(sa.Integer, default=0)
	nettobetrag = sa.Column(sa.Numeric, default=0)
	paid_flag = sa.Column(sa.Integer, default=0)
	prtflag = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	sysdate = sa.Column(sa.Date, default=get_current_date())
	tischnr = sa.Column(sa.Integer, default=0)
	transferred = sa.Column(sa.Boolean, default=False)
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('bill_datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('epreis', 0)
		kwargs.setdefault('fremdwbetrag', 0)
		kwargs.setdefault('kellner_nr', 0)
		kwargs.setdefault('nettobetrag', 0)
		kwargs.setdefault('paid_flag', 0)
		kwargs.setdefault('prtflag', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('steuercode', 0)
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('tischnr', 0)
		kwargs.setdefault('transferred', False)
		kwargs.setdefault('waehrungsnr', 0)
		kwargs.setdefault('zeit', 0)
		super(H_bill_line, self).__init__(*args, **kwargs)
