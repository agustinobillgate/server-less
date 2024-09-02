from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hrsegement(Base):
	__tablename__ = 'hrsegement'

	betriebsnr = sa.Column(sa.Integer, default=0)
	couverts_eff = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	tischanz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
