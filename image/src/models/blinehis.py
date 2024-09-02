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
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	userinit = sa.Column(sa.String, default="")
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
