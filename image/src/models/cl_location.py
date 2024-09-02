from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_location(Base):
	__tablename__ = 'cl_location'

	activeflag = sa.Column(sa.Boolean, default=False)
	child_num = sa.Column(sa.Integer, default=0)
	from_time = sa.Column(sa.String, default="0000")
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	parent = sa.Column(sa.Integer, default=0)
	to_time = sa.Column(sa.String, default="2400")
	_recid = sa.Column(sa.Integer, primary_key=True)
