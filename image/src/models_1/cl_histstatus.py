#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_histstatus(Base):
	__tablename__ = 'cl_histstatus'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	datum1 = sa.Column(sa.Date, default=None)
	datum2 = sa.Column(sa.Date, default=None)
	freeze_for = sa.Column(sa.Integer, default=0)
	memstatus = sa.Column(sa.Integer, default=0)
	memtype1 = sa.Column(sa.Integer, default=0)
	memtype2 = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.String, default="")
	remark = sa.Column(sa.String, default="")
	user_init = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('codenum', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('datum1', None)
		kwargs.setdefault('datum2', None)
		kwargs.setdefault('freeze_for', 0)
		kwargs.setdefault('memstatus', 0)
		kwargs.setdefault('memtype1', 0)
		kwargs.setdefault('memtype2', 0)
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', "")
		kwargs.setdefault('remark', "")
		kwargs.setdefault('user_init', "")
		kwargs.setdefault('zeit', 0)
		super(Cl_histstatus, self).__init__(*args, **kwargs)
