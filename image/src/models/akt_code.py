from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Akt_code(Base):
	__tablename__ = 'akt_code'

	aktiongrup = sa.Column(sa.Integer, default=1)
	aktionscode = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	flag = sa.Column(sa.Integer, default=0)
	int1 = sa.Column(sa.Integer, default=0)
	int2 = sa.Column(sa.Integer, default=0)
	int3 = sa.Column(sa.Integer, default=0)
	korrespondenz = sa.Column(sa.Boolean, default=False)
	wertigkeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
