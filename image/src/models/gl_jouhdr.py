#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_jouhdr(Base):
	__tablename__ = 'gl_jouhdr'

	activeflag = sa.Column(sa.Integer, default=0)
	batch = sa.Column(sa.Boolean, default=False)
	bezeich = sa.Column(sa.String, default="")
	credit = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	debit = sa.Column(sa.Numeric, default=0)
	jnr = sa.Column(sa.Integer, default=0)
	jtype = sa.Column(sa.Integer, default=0)
	refno = sa.Column(sa.String, default="")
	remain = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('activeflag', 0)
		kwargs.setdefault('batch', False)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('credit', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('debit', 0)
		kwargs.setdefault('jnr', 0)
		kwargs.setdefault('jtype', 0)
		kwargs.setdefault('refno', "")
		kwargs.setdefault('remain', 0)
		super(Gl_jouhdr, self).__init__(*args, **kwargs)
