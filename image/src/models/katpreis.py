from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Katpreis(Base):
	__tablename__ = 'katpreis'

	argtnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	endperiode = sa.Column(sa.Date, default=None)
	kindpreis = sa.Column(ARRAY(sa.Numeric),default=[0,0])
	perspreis = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0])
	startperiode = sa.Column(sa.Date, default=None)
	zikatnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
