#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Akt_cust(Base):
	__tablename__ = 'akt_cust'

	c_init = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=get_current_date())
	gastnr = sa.Column(sa.Integer, default=None)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('c_init', "")
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('userinit', "")
		super(Akt_cust, self).__init__(*args, **kwargs)
