from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class B_storno(Base):
	__tablename__ = 'b_storno'

	bankettnr = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	breslinnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	gastnr = sa.Column(sa.Integer, default=0)
	grund = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","",""])
	usercode = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
