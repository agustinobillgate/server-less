#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_department(Base):
	__tablename__ = 'gl_department'

	bezeich = sa.Column(sa.String, default="")
	fodept = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('fodept', 0)
		kwargs.setdefault('nr', 0)
		super(Gl_department, self).__init__(*args, **kwargs)
