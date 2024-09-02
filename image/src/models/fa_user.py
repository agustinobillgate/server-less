from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_user(Base):
	__tablename__ = 'fa_user'

	anzahl = sa.Column(sa.Integer, default=0)
	bis_datum = sa.Column(sa.Date, default=None)
	chgid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=lambda: get_current_date())
	createdid = sa.Column(sa.String, default="")
	fa_status = sa.Column(sa.Integer, default=0)
	modifed = sa.Column(sa.Date, default=None)
	nr = sa.Column(sa.Integer, default=0)
	rcvid = sa.Column(sa.String, default="")
	rcvname = sa.Column(sa.String, default="")
	released = sa.Column(sa.Date, default=None)
	res_char = sa.Column(ARRAY(sa.String),default=["","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	res_logi = sa.Column(ARRAY(sa.Boolean),default=[False,False,False])
	vom_datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
