from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_ophhis(Base):
	__tablename__ = 'l_ophhis'

	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	docu_nr = sa.Column(sa.String, default="")
	fibukonto = sa.Column(sa.String, default="")
	lscheinnr = sa.Column(sa.String, default="")
	op_typ = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
