from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_reqif(Base):
	__tablename__ = 'eg_reqif'

	category = sa.Column(sa.String, default="")
	email = sa.Column(sa.String, default="")
	frm_dept = sa.Column(sa.String, default="")
	frm_usr = sa.Column(sa.String, default="")
	mobile_ph = sa.Column(sa.String, default="")
	pager = sa.Column(sa.String, default="")
	reqnr = sa.Column(sa.Integer, default=0)
	request_date = sa.Column(sa.Date, default=None)
	reserve_char = sa.Column(sa.String, default="")
	reserve_date = sa.Column(sa.Date, default=None)
	reserve_int = sa.Column(sa.Integer, default=0)
	reserve_log = sa.Column(sa.Boolean, default=False)
	rstatus = sa.Column(sa.Integer, default=0)
	sent_date = sa.Column(sa.Date, default=None)
	sent_time = sa.Column(sa.Integer, default=0)
	source = sa.Column(sa.String, default="")
	sub_taskdesc = sa.Column(sa.String, default="")
	task_def = sa.Column(sa.String, default="")
	task_solution = sa.Column(sa.String, default="")
	to_dept = sa.Column(sa.String, default="")
	to_usr = sa.Column(sa.String, default="")
	type = sa.Column(sa.Integer, default=0)
	usr_id = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
