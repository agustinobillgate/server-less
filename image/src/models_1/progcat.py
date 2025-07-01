#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Progcat(Base):
	__tablename__ = 'progcat'

	bezeich = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	password = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('password', "")
		super(Progcat, self).__init__(*args, **kwargs)
