#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Htreport(Base):
	__tablename__ = 'htreport'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	conparam = sa.Column(sa.String, default="")
	libname = sa.Column(sa.String, default="")
	libpath = sa.Column(sa.String, default="")
	repname = sa.Column(sa.String, default="")
	repnr = sa.Column(sa.Integer, default=0)
	sprache = sa.Column(sa.Integer, default=0)
	wintitle = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('conparam', "")
		kwargs.setdefault('libname', "")
		kwargs.setdefault('libpath', "")
		kwargs.setdefault('repname', "")
		kwargs.setdefault('repnr', 0)
		kwargs.setdefault('sprache', 0)
		kwargs.setdefault('wintitle', "")
		super(Htreport, self).__init__(*args, **kwargs)
