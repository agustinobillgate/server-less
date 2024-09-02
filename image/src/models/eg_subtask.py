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
