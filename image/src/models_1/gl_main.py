#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_main(Base):
	__tablename__ = 'gl_main'

	bezeich = sa.Column(sa.String, default="")
	code = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	type_code = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('code', 0)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('type_code', "")
		super(Gl_main, self).__init__(*args, **kwargs)
