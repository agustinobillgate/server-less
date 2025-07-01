#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Archieve(Base):
	__tablename__ = 'archieve'

	char = sa.Column(ARRAY(sa.String),default=["","","","",""])
	datum = sa.Column(sa.Date, default=None)
	key = sa.Column(sa.String, default="")
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('char', ["","","","",""])
		kwargs.setdefault('datum', None)
		kwargs.setdefault('key', "")
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', 0)
		kwargs.setdefault('num3', 0)
		super(Archieve, self).__init__(*args, **kwargs)
