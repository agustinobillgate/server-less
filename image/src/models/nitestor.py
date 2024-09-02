from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nitestor(Base):
	__tablename__ = 'nitestor'

	betriebsnr = sa.Column(sa.Integer, default=0)
	line = sa.Column(sa.String, default="")
	line_nr = sa.Column(sa.Integer, default=0)
	night_type = sa.Column(sa.Integer, default=0)
	reihenfolge = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
