#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_coa(Base):
	__tablename__ = 'gl_coa'

	acc_type = sa.Column(sa.Integer, default=0)
	activeflag = sa.Column(sa.Boolean, default=False)
	actual = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	b_flag = sa.Column(sa.Boolean, default=False)
	bemerk = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	budget = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	c_date = sa.Column(sa.Date, default=None)
	chginit = sa.Column(sa.String, default="")
	credit = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	debit = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	deptnr = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="0000000000")
	fs_type = sa.Column(sa.Integer, default=0)
	last_yr = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	ly_budget = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0])
	m_date = sa.Column(sa.Date, default=None)
	main_nr = sa.Column(sa.Integer, default=0)
	modifiable = sa.Column(sa.Boolean, default=True)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('acc_type', 0)
		kwargs.setdefault('activeflag', False)
		kwargs.setdefault('actual', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('b_flag', False)
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('budget', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('c_date', None)
		kwargs.setdefault('chginit', "")
		kwargs.setdefault('credit', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('debit', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('deptnr', 0)
		kwargs.setdefault('fibukonto', "0000000000")
		kwargs.setdefault('fs_type', 0)
		kwargs.setdefault('last_yr', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('ly_budget', [0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('m_date', None)
		kwargs.setdefault('main_nr', 0)
		kwargs.setdefault('modifiable', True)
		kwargs.setdefault('userinit', "")
		super(Gl_coa, self).__init__(*args, **kwargs)
