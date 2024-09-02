from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Notes(Base):
	__tablename__ = 'notes'

	bediener_nr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	dept = sa.Column(sa.String, default="")
	note = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","","",""])
	page_nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
