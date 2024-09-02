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
