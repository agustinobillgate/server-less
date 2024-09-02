from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Rg_reports(Base):
	__tablename__ = 'rg_reports'

	activeflag = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	col_dim = sa.Column(sa.String, default="")
	created_by = sa.Column(sa.String, default="")
	created_date = sa.Column(sa.Date, default=None)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	facts_dim = sa.Column(sa.String, default="")
	form_dim = sa.Column(sa.String, default="")
	last_updated = sa.Column(sa.Date, default=None)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	metadata_ = sa.Column('metadata', sa.String)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	out_dim = sa.Column(sa.String, default="")
	overwrite_by = sa.Column(sa.String, default="")
	ovwrite_by_group = sa.Column(sa.String, default="")
	report_group = sa.Column(sa.Integer, default=0)
	report_sub = sa.Column(sa.Integer, default=0)
	report_title = sa.Column(sa.String, default="")
	reportnr = sa.Column(sa.Integer, default=0)
	row_dim = sa.Column(sa.String, default="")
	slice_name = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	updated_by = sa.Column(sa.String, default="")
	usercode = sa.Column(sa.String, default="")
	usr_access = sa.Column(sa.String, default="")
	view_name = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	visible_to_group = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
