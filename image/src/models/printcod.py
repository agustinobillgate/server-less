from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Printcod(Base):
	__tablename__ = 'printcod'

	bezeichnung = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	contcode = sa.Column(sa.String, default="")
	emu = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
