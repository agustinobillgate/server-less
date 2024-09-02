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
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	tischnr = sa.Column(sa.Integer, default=0)
	transferred = sa.Column(sa.Boolean, default=False)
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
