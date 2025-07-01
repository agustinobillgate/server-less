#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_cost(Base):
	__tablename__ = 'gl_cost'

	b_betrag = sa.Column(sa.Numeric, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	f_betrag = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('b_betrag', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('f_betrag', 0)
		kwargs.setdefault('fibukonto', "")
		super(Gl_cost, self).__init__(*args, **kwargs)
