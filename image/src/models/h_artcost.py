from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_artcost(Base):
	__tablename__ = 'h_artcost'

	anzahl = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	cost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	lm_anzahl = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	lm_cost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	_recid = sa.Column(sa.Integer, primary_key=True)
