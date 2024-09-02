from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bill_lin_tax(Base):
	__tablename__ = 'bill_lin_tax'

	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	billin_nr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	stererpct = sa.Column(sa.Numeric, default=0)
	steuer_betrag = sa.Column(sa.Numeric, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
