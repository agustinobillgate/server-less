from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hotel_server(Base):
	__tablename__ = 'hotel_server'

	appserver = sa.Column(sa.String, default="")
	device_name = sa.Column(sa.String, default="")
	id = sa.Column(sa.Integer, default=0)
	update_now_flag = sa.Column(sa.Boolean, default=False)
	update_status = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
