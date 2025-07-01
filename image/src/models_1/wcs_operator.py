from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Wcs_operator(Base):
	__tablename__ = 'wcs_operator'

	id = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
