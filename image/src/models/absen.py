from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Absen(Base):
	__tablename__ = 'absen'

	abstatus = sa.Column(sa.Integer, default=0)
	anrede = sa.Column(sa.String, default="")
	box_no = sa.Column(sa.String, default="")
	carnr = sa.Column(sa.String, default="")
	ci_date = sa.Column(sa.Date, default=lambda: get_current_date())
	ci_id = sa.Column(sa.String, default="")
	ci_time = sa.Column(sa.String, default="")
	co_date = sa.Column(sa.Date, default=None)
	co_id = sa.Column(sa.String, default="")
	co_time = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=None)
	gtype = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	resline = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	total_adult = sa.Column(ARRAY(sa.Integer),default=[0,0])
	total_child = sa.Column(ARRAY(sa.Integer),default=[0,0])
	total_infant = sa.Column(ARRAY(sa.Integer),default=[0,0])
	vorname = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
