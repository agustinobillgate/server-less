from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_jourhis(Base):
	__tablename__ = 'gl_jourhis'

	activeflag = sa.Column(sa.Integer, default=0)
	bemerk = sa.Column(sa.String, default="")
	chgdate = sa.Column(sa.Date, default=None)
	chginit = sa.Column(sa.String, default="")
	credit = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	debit = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	jnr = sa.Column(sa.Integer, default=0)
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
