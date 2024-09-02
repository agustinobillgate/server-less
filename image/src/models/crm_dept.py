from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Crm_dept(Base):
	__tablename__ = 'crm_dept'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	char4 = sa.Column(sa.String, default="")
	char5 = sa.Column(sa.String, default="")
	confirmflag = sa.Column(sa.Boolean, default=False)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	date4 = sa.Column(sa.Date, default=None)
	date5 = sa.Column(sa.Date, default=None)
	dept_nr = sa.Column(sa.Integer, default=0)
	dname = sa.Column(sa.String, default="")
	hno = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	logi4 = sa.Column(sa.Boolean, default=False)
	logi5 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	number4 = sa.Column(sa.Integer, default=0)
	number5 = sa.Column(sa.Integer, default=0)
	sentdate = sa.Column(sa.Date, default=None)
	sentflag = sa.Column(sa.Boolean, default=False)
	senttime = sa.Column(sa.Integer, default=0)
	statusflag = sa.Column(sa.Integer, default=0)
	webconfirmflag = sa.Column(sa.Boolean, default=False)
	websentflag = sa.Column(sa.Boolean, default=False)
	webstatusflag = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
