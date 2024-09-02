from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Akt_line(Base):
	__tablename__ = 'akt_line'

	aktionscode = sa.Column(sa.Integer, default=0)
	aktnr = sa.Column(sa.Integer, default=0)
	bemerk = sa.Column(sa.String, default="")
	briefnr = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	chg_datum = sa.Column(sa.Date, default=lambda: get_current_date())
	chg_id = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	dauer = sa.Column(sa.Integer, default=0)
	dec1 = sa.Column(sa.Numeric, default=0)
	dec2 = sa.Column(sa.Numeric, default=0)
	flag = sa.Column(sa.Integer, default=0)
	fname = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=0)
	grupnr = sa.Column(sa.Integer, default=0)
	int1 = sa.Column(sa.Integer, default=0)
	int2 = sa.Column(sa.Integer, default=0)
	int3 = sa.Column(sa.Integer, default=0)
	int4 = sa.Column(sa.Integer, default=0)
	kontakt = sa.Column(sa.String, default="")
	kontakt_nr = sa.Column(sa.Integer, default=0)
	linenr = sa.Column(sa.Integer, default=0)
	location = sa.Column(sa.String, default="")
	prioritaet = sa.Column(sa.Integer, default=0)
	regard = sa.Column(sa.String, default="")
	results = sa.Column(sa.String, default="")
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
