#version: 1.0.0.2

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bondrucker', False)
		kwargs.setdefault('copies', 1)
		kwargs.setdefault('emu', "")
		kwargs.setdefault('make', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('opsysname', "")
		kwargs.setdefault('path', "")
		kwargs.setdefault('pglen', 0)
		kwargs.setdefault('position', "")
		kwargs.setdefault('spooled', False)
		super(Printer, self).__init__(*args, **kwargs)
