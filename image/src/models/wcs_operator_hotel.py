from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Wcs_operator_hotel(Base):
	__tablename__ = 'wcs_operator_hotel'

	hotel_id = sa.Column(sa.Integer, default=0)
	operator_id = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
