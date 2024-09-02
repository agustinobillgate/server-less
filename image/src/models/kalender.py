from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kalender(Base):
	__tablename__ = 'kalender'

	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	dept = sa.Column(sa.String, default="")
	note = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","","",""])
	_recid = sa.Column(sa.Integer, primary_key=True)
