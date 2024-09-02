from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_zahlbed(Base):
	__tablename__ = 'l_zahlbed'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	skonto_perc = sa.Column(sa.Numeric, default=0)
	skonto_tage = sa.Column(sa.Integer, default=0)
	z_code = sa.Column(sa.String, default="")
	zahl_ziel = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
