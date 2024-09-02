from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bill_line(Base):
	__tablename__ = 'bill_line'

	anzahl = sa.Column(sa.Integer, default=0)
	arrangement = sa.Column(sa.String, default="")
	artnr = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	bill_datum = sa.Column(sa.Date, default=None)
	billin_nr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	fremdwbetrag = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	massnr = sa.Column(sa.Integer, default=0)
	mwstsplit = sa.Column(sa.Boolean, default=False)
	nettobetrag = sa.Column(sa.Numeric, default=0)
	origin_id = sa.Column(sa.String, default="")
	orts_tax = sa.Column(sa.Numeric, default=0)
	printflag = sa.Column(sa.Integer, default=0)
	prtflag = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	tax_booked = sa.Column(sa.Boolean, default=False)
	typ = sa.Column(sa.Integer, default=0)
	userinit = sa.Column(sa.String, default="")
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
