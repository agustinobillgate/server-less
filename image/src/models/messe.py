from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Messe(Base):
	__tablename__ = 'messe'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	mdatum = sa.Column(sa.Date, default=None)
	mtext = sa.Column(sa.String, default="")
	notes = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
