from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_acct(Base):
	__tablename__ = 'gl_acct'

	acc_type = sa.Column(sa.Integer, default=0)
	activeflag = sa.Column(sa.Boolean, default=False)
	actual = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	b_flag = sa.Column(sa.Boolean, default=False)
	bemerk = sa.Column(sa.String, default="")
	bezeich = sa.Column(sa.String, default="")
	budget = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	c_date = sa.Column(sa.Date, default=None)
	chginit = sa.Column(sa.String, default="")
	credit = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	debit = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	deptnr = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="0000000000000")
	fs_type = sa.Column(sa.Integer, default=0)
	last_yr = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	ly_budget = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	m_date = sa.Column(sa.Date, default=None)
	main_nr = sa.Column(sa.Integer, default=0)
	modifiable = sa.Column(sa.Boolean, default=True)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
