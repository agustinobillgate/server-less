from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_cost(Base):
	__tablename__ = 'gl_cost'

	b_betrag = sa.Column(sa.Numeric, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=None)
	f_betrag = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
