from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sources(Base):
	__tablename__ = 'sources'

	betriebsnr = sa.Column(sa.Integer, default=0)
	budlogis = sa.Column(sa.Numeric, default=0)
	budpersanz = sa.Column(sa.Integer, default=0)
	budzimmeranz = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	logis = sa.Column(sa.Numeric, default=0)
	persanz = sa.Column(sa.Integer, default=0)
	source_code = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
