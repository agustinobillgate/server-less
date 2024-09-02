from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Exrate(Base):
	__tablename__ = 'exrate'

	artnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
