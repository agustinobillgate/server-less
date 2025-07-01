#version: 1.0.0.2

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
	geaendert = sa.Column(sa.Date, default=get_current_date())
	travelers_chk = sa.Column(sa.Numeric, default=0)
	verkauf = sa.Column(sa.Numeric, default=0)
	wabkurz = sa.Column(sa.String, default="")
	waehrungsnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('ankauf', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('cash_comm', 0)
		kwargs.setdefault('cheque_comm', 0)
		kwargs.setdefault('einheit', 1)
		kwargs.setdefault('geaendert', get_current_date())
		kwargs.setdefault('travelers_chk', 0)
		kwargs.setdefault('verkauf', 0)
		kwargs.setdefault('wabkurz', "")
		kwargs.setdefault('waehrungsnr', 0)
		super(Waehrung, self).__init__(*args, **kwargs)
