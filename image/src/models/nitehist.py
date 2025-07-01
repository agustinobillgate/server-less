#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nitehist(Base):
	__tablename__ = 'nitehist'

	datum = sa.Column(sa.Date, default=None)
	line = sa.Column(sa.String, default="")
	line_nr = sa.Column(sa.Integer, default=0)
	reihenfolge = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('datum', None)
		kwargs.setdefault('line', "")
		kwargs.setdefault('line_nr', 0)
		kwargs.setdefault('reihenfolge', 0)
		super(Nitehist, self).__init__(*args, **kwargs)
