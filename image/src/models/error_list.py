from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Error_list(Base):
	__tablename__ = 'error_list'

	error_time = sa.Column(sa.DateTime, default=None)
	hotel_id = sa.Column(sa.Integer, default=0)
	last_update = sa.Column(sa.DateTime, default=None)
	prog_name = sa.Column(sa.String, default="")
	str = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
