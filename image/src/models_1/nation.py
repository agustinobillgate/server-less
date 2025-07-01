#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nation(Base):
	__tablename__ = 'nation'

	bezeich = sa.Column(sa.String, default="")
	hauptgruppe = sa.Column(sa.Integer, default=1)
	in_stat = sa.Column(sa.Boolean, default=False)
	kurzbez = sa.Column(sa.String, default="")
	language = sa.Column(sa.Integer, default=0)
	natcode = sa.Column(sa.Integer, default=0)
	nationnr = sa.Column(sa.Integer, default=0)
	untergruppe = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('hauptgruppe', 1)
		kwargs.setdefault('in_stat', False)
		kwargs.setdefault('kurzbez', "")
		kwargs.setdefault('language', 0)
		kwargs.setdefault('natcode', 0)
		kwargs.setdefault('nationnr', 0)
		kwargs.setdefault('untergruppe', 1)
		super(Nation, self).__init__(*args, **kwargs)
