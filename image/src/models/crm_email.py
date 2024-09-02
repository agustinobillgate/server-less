from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Crm_email(Base):
	__tablename__ = 'crm_email'

	attachment = sa.Column(sa.String, default="")
	body = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	cnr = sa.Column(sa.Integer, default=0)
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	email = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=0)
	guestname = sa.Column(sa.String, default="")
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	s_status = sa.Column(sa.Integer, default=0)
	subject = sa.Column(sa.String, default="")
	usrid = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
