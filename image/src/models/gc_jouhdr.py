from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gc_jouhdr(Base):
	__tablename__ = 'gc_jouhdr'

	activeflag = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	credit = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	debit = sa.Column(sa.Numeric, default=0)
	jnr = sa.Column(sa.Integer, default=0)
	refno = sa.Column(sa.String, default="")
	remain = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
