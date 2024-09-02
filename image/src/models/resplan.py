from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Resplan(Base):
	__tablename__ = 'resplan'

	anzzim = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0,0,0,0,0])
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	zikatnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
