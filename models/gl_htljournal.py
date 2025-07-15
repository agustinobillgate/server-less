#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_htljournal(Base):
	__tablename__ = 'gl_htljournal'

	datum = sa.Column(sa.Date, default=None)
	htl_jnr = sa.Column(sa.Integer, default=0)
	htl_license = sa.Column(sa.String, default="")
	jnr = sa.Column(sa.Integer, default=0)
	vstring = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('datum', None)
		kwargs.setdefault('htl_jnr', 0)
		kwargs.setdefault('htl_license', "")
		kwargs.setdefault('jnr', 0)
		kwargs.setdefault('vstring', "")
		super(Gl_htljournal, self).__init__(*args, **kwargs)
