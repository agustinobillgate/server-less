from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guestat1(Base):
	__tablename__ = 'guestat1'

	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=None)
	logis = sa.Column(sa.Numeric, default=0)
	persanz = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
