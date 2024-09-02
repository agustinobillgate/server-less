from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Parameters(Base):
	__tablename__ = 'parameters'

	progname = sa.Column(sa.String, default="")
	section = sa.Column(sa.String, default="")
	varname = sa.Column(sa.String, default="")
	vstring = sa.Column(sa.String, default="")
	vtype = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
