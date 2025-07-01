from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hotel(Base):
	__tablename__ = 'hotel'

	ai_busy = sa.Column(sa.Integer, default=0)
	ai_empty = sa.Column(sa.Integer, default=0)
	ai_full = sa.Column(sa.Integer, default=0)
	ai_locked = sa.Column(sa.Integer, default=0)
	appserver = sa.Column(sa.String, default="")
	appserver2 = sa.Column(sa.String, default="")
	available_qty = sa.Column(sa.Integer, default=0)
	check_now_flag = sa.Column(sa.Boolean, default=False)
	connect_flag = sa.Column(sa.Boolean, default=False)
	id = sa.Column(sa.Integer, default=0)
	ip = sa.Column(sa.String, default="")
	last_error_check = sa.Column(sa.DateTime, default=None)
	last_update = sa.Column(sa.DateTime, default=None)
	locked_last_change = sa.Column(sa.Integer, default=0)
	locked_qty = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	port = sa.Column(sa.Integer, default=0)
	receiving_last_change = sa.Column(sa.Integer, default=0)
	receiving_qty = sa.Column(sa.Integer, default=0)
	running_last_change = sa.Column(sa.Integer, default=0)
	running_qty = sa.Column(sa.Integer, default=0)
	sending_last_change = sa.Column(sa.Integer, default=0)
	sending_qty = sa.Column(sa.Integer, default=0)
	server_id = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
