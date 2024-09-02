from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guestat(Base):
	__tablename__ = 'guestat'

	argtumsatz = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	f_b_umsatz = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	jahr = sa.Column(sa.Integer, default=0)
	logisumsatz = sa.Column(sa.Numeric, default=0)
	monat = sa.Column(sa.Integer, default=0)
	room_nights = sa.Column(sa.Integer, default=0)
	sonst_umsatz = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
