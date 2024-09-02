from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Arrangement(Base):
	__tablename__ = 'arrangement'

	argt_artikelnr = sa.Column(sa.Integer, default=0)
	argt_bez = sa.Column(sa.String, default="")
	argt_preis = sa.Column(sa.Numeric, default=0)
	argt_rgbez = sa.Column(sa.String, default="")
	argt_rgbez2 = sa.Column(ARRAY(sa.String),default=["","","",""])
	argt_typ = sa.Column(sa.Integer, default=0)
	argtnr = sa.Column(sa.Integer, default=0)
	arrangement = sa.Column(sa.String, default="")
	arrangement_art = sa.Column(sa.Integer, default=0)
	artnr_logis = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	fakt_modus = sa.Column(sa.Integer, default=1)
	fixpreisargt = sa.Column(sa.Boolean, default=False)
	handtuch = sa.Column(sa.Integer, default=0)
	intervall = sa.Column(sa.Integer, default=0)
	logis_preis = sa.Column(sa.Numeric, default=0)
	logis_proz = sa.Column(sa.Numeric, default=0)
	mwstsplit = sa.Column(sa.Boolean, default=False)
	options = sa.Column(sa.String, default="")
	segmentcode = sa.Column(sa.Integer, default=0)
	ventil = sa.Column(sa.Boolean, default=False)
	waeschewechsel = sa.Column(sa.Integer, default=0)
	weeksplit = sa.Column(sa.Boolean, default=False)
	zuordnung = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
