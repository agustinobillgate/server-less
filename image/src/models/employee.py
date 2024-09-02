from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Employee(Base):
	__tablename__ = 'employee'

	accno = sa.Column(sa.String, default="")
	activeflag = sa.Column(sa.Boolean, default=False)
	address1 = sa.Column(sa.String, default="")
	address2 = sa.Column(sa.String, default="")
	allowance = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False])
	bank = sa.Column(sa.String, default="")
	ben_eat = sa.Column(sa.Numeric, default=0)
	ben_trans = sa.Column(sa.Numeric, default=0)
	birthdate = sa.Column(sa.Date, default=None)
	branch = sa.Column(sa.String, default="")
	bsalary = sa.Column(sa.Numeric, default=0)
	cbirth = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None])
	child = sa.Column(ARRAY(sa.String),default=["","","","",""])
	city = sa.Column(sa.String, default="")
	degree = sa.Column(sa.Integer, default=0)
	dept = sa.Column(sa.Integer, default=0)
	doct = sa.Column(sa.Numeric, default=0)
	estat = sa.Column(sa.Integer, default=0)
	fname = sa.Column(sa.String, default="")
	gender = sa.Column(sa.Integer, default=0)
	hdate = sa.Column(sa.Date, default=lambda: get_current_date())
	id = sa.Column(sa.String, default="")
	idcard = sa.Column(sa.String, default="")
	imgfile = sa.Column(sa.String, default="")
	mstat = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	nation = sa.Column(sa.String, default="")
	partner = sa.Column(sa.String, default="")
	pbirth = sa.Column(sa.Date, default=None)
	position = sa.Column(sa.String, default="")
	religion = sa.Column(sa.Integer, default=0)
	tdate = sa.Column(sa.Date, default=None)
	telephone = sa.Column(sa.String, default="")
	zipcode = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
