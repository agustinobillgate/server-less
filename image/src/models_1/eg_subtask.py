#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_subtask(Base):
	__tablename__ = 'eg_subtask'

	bezeich = sa.Column(sa.String, default="")
	create_by = sa.Column(sa.String, default="")
	create_date = sa.Column(sa.Date, default=None)
	create_time = sa.Column(sa.Integer, default=0)
	dept_nr = sa.Column(sa.Integer, default=0)
	dur_nr = sa.Column(sa.Integer, default=0)
	main_nr = sa.Column(sa.Integer, default=0)
	othersflag = sa.Column(sa.Boolean, default=False)
	reserve_char = sa.Column(sa.String, default="")
	reserve_date = sa.Column(sa.Date, default=None)
	reserve_int = sa.Column(sa.Integer, default=0)
	reserve_log = sa.Column(sa.Boolean, default=False)
	sourceform = sa.Column(sa.String, default="")
	sub_code = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('create_by', "")
		kwargs.setdefault('create_date', None)
		kwargs.setdefault('create_time', 0)
		kwargs.setdefault('dept_nr', 0)
		kwargs.setdefault('dur_nr', 0)
		kwargs.setdefault('main_nr', 0)
		kwargs.setdefault('othersflag', False)
		kwargs.setdefault('reserve_char', "")
		kwargs.setdefault('reserve_date', None)
		kwargs.setdefault('reserve_int', 0)
		kwargs.setdefault('reserve_log', False)
		kwargs.setdefault('sourceform', "")
		kwargs.setdefault('sub_code', "")
		super(Eg_subtask, self).__init__(*args, **kwargs)
