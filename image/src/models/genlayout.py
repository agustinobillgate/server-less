from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Genlayout(Base):
	__tablename__ = 'genlayout'

	activeflag = sa.Column(sa.Boolean, default=True)
	add_height = sa.Column(sa.Numeric, default=0)
	add_width = sa.Column(sa.Numeric, default=0)
	button_ext = sa.Column(ARRAY(sa.String),default=["","","","","",""])
	canc_height = sa.Column(sa.Numeric, default=0)
	canc_width = sa.Column(sa.Numeric, default=0)
	char_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	combo_ext = sa.Column(ARRAY(sa.String),default=["","",""])
	date_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	deci_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	del_height = sa.Column(sa.Numeric, default=0)
	del_width = sa.Column(sa.Numeric, default=0)
	exit_height = sa.Column(sa.Numeric, default=0)
	exit_width = sa.Column(sa.Numeric, default=0)
	frame_height = sa.Column(sa.Numeric, default=0)
	frame_title = sa.Column(sa.String, default="")
	frame_width = sa.Column(sa.Numeric, default=0)
	inte_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	key = sa.Column(sa.String, default="")
	logi_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	string_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	tchar_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	tdate_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	tdeci_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	tinte_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	tlogi_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	_recid = sa.Column(sa.Integer, primary_key=True)
