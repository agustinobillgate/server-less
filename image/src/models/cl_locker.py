from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_locker(Base):
	__tablename__ = 'cl_locker'

	card_num = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	from_date = sa.Column(sa.Date, default=lambda: get_current_date())
	from_time = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.Integer, default=0)
	locknum = sa.Column(sa.String, default="")
	to_date = sa.Column(sa.Date, default=lambda: get_current_date())
	to_time = sa.Column(sa.Integer, default=0)
	towel = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	towel_in = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	towel_out = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	userinit = sa.Column(sa.String, default="")
	valid_flag = sa.Column(sa.Boolean, default=True)
	_recid = sa.Column(sa.Integer, primary_key=True)
