#version: 1.0.0.3

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('attachment', "")
		kwargs.setdefault('body', "")
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('cnr', 0)
		kwargs.setdefault('date1', None)
		kwargs.setdefault('date2', None)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('email', "")
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('guestname', "")
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('number2', 0)
		kwargs.setdefault('number3', 0)
		kwargs.setdefault('s_status', 0)
		kwargs.setdefault('subject', "")
		kwargs.setdefault('usrid', "")
		kwargs.setdefault('zeit', 0)
		super(Crm_email, self).__init__(*args, **kwargs)
