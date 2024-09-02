from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Waehrung(Base):
	__tablename__ = 'waehrung'

	ankauf = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	cash_comm = sa.Column(sa.Numeric, default=0)
	cheque_comm = sa.Column(sa.Numeric, default=0)
	einheit = sa.Column(sa.Integer, default=1)
	geaendert = sa.Column(sa.Date, default=lambda: get_current_date())
	travelers_chk = sa.Column(sa.Numeric, default=0)
	verkauf = sa.Column(sa.Numeric, default=0)
	wabkurz = sa.Column(sa.String, default="")
	waehrungsnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
