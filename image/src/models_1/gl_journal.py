#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_journal(Base):
	__tablename__ = 'gl_journal'

	activeflag = sa.Column(sa.Integer, default=0)
	bemerk = sa.Column(sa.String, default="")
	chgdate = sa.Column(sa.Date, default=None)
	chginit = sa.Column(sa.String, default="")
	credit = sa.Column(sa.Numeric, default=0)
	debit = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	jnr = sa.Column(sa.Integer, default=0)
	sysdate = sa.Column(sa.Date, default=get_current_date())
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', 0)
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('chgdate', None)
		kwargs.setdefault('chginit', "")
		kwargs.setdefault('credit', 0)
		kwargs.setdefault('debit', 0)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('jnr', 0)
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('zeit', 0)
		super(Gl_journal, self).__init__(*args, **kwargs)
