#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_grup(Base):
	__tablename__ = 'fa_grup'

	bezeich = sa.Column(sa.String, default="")
	credit_fibu = sa.Column(sa.String, default="")
	debit_fibu = sa.Column(sa.String, default="")
	fibukonto = sa.Column(sa.String, default="")
	flag = sa.Column(sa.Integer, default=0)
	gnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('credit_fibu', "")
		kwargs.setdefault('debit_fibu', "")
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('gnr', 0)
		super(Fa_grup, self).__init__(*args, **kwargs)
