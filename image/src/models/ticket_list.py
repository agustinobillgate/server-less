from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ticket_list(Base):
	__tablename__ = 'ticket_list'

	id = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
