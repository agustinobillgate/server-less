#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Parameters(Base):
	__tablename__ = 'parameters'

	progname = sa.Column(sa.String, default="")
	section = sa.Column(sa.String, default="")
	varname = sa.Column(sa.String, default="")
	vstring = sa.Column(sa.String, default="")
	vtype = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('progname', "")
		kwargs.setdefault('section', "")
		kwargs.setdefault('varname', "")
		kwargs.setdefault('vstring', "")
		kwargs.setdefault('vtype', 0)
		super(Parameters, self).__init__(*args, **kwargs)
