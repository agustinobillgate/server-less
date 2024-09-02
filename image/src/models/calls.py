from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Calls(Base):
	__tablename__ = 'calls'

	aufschlag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	buchflag = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	dauer = sa.Column(sa.Integer, default=0)
	gastbetrag = sa.Column(sa.Numeric, default=0)
	impulse = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	leitung = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	pabxbetrag = sa.Column(sa.Numeric, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	rufnummer = sa.Column(sa.String, default="")
	satz_id = sa.Column(sa.String, default="")
	sequence = sa.Column(sa.Integer, default=0)
	transdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	transzeit = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
