from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Crm_language(Base):
	__tablename__ = 'crm_language'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	confirmflag = sa.Column(sa.Boolean, default=False)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	defaults = sa.Column(sa.Boolean, default=False)
	description = sa.Column(sa.String, default="")
	hno = sa.Column(sa.Integer, default=0)
	int1 = sa.Column(sa.Integer, default=0)
	int2 = sa.Column(sa.Integer, default=0)
	int3 = sa.Column(sa.Integer, default=0)
	language_nr = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	sentdate = sa.Column(sa.Date, default=None)
	sentflag = sa.Column(sa.Boolean, default=False)
	senttime = sa.Column(sa.Integer, default=0)
	shortdesc = sa.Column(sa.String, default="")
	statusflag = sa.Column(sa.Integer, default=0)
	webconfirmflag = sa.Column(sa.Boolean, default=False)
	websentflag = sa.Column(sa.Boolean, default=False)
	webstatusflag = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
