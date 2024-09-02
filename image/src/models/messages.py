from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Messages(Base):
	__tablename__ = 'messages'

	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	gastnr = sa.Column(sa.Integer, default=None)
	messtext = sa.Column(ARRAY(sa.String),default=["","","","","","","","","",""])
	name = sa.Column(sa.String, default="")
	present_guest = sa.Column(sa.Boolean, default=False)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	usre = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
