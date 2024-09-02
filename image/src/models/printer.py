from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Printer(Base):
	__tablename__ = 'printer'

	bondrucker = sa.Column(sa.Boolean, default=False)
	copies = sa.Column(sa.Integer, default=1)
	emu = sa.Column(sa.String, default="")
	make = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	opsysname = sa.Column(sa.String, default="")
	path = sa.Column(sa.String, default="")
	pglen = sa.Column(sa.Integer, default=0)
	position = sa.Column(sa.String, default="")
	spooled = sa.Column(sa.Boolean, default=False)
	_recid = sa.Column(sa.Integer, primary_key=True)
