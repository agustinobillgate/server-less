from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_lieferant(Base):
	__tablename__ = 'l_lieferant'

	adresse1 = sa.Column(sa.String, default="")
	adresse2 = sa.Column(sa.String, default="")
	adresse3 = sa.Column(sa.String, default="")
	anrede1 = sa.Column(sa.String, default="")
	anredefirma = sa.Column(sa.String, default="")
	bank = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	blz = sa.Column(sa.String, default="")
	fax = sa.Column(sa.String, default="")
	firma = sa.Column(sa.String, default="")
	kontonr = sa.Column(sa.String, default="")
	land = sa.Column(sa.String, default="")
	lief_nr = sa.Column(sa.Integer, default=0)
	lieferdatum = sa.Column(sa.Date, default=None)
	namekontakt = sa.Column(sa.String, default="")
	notizen = sa.Column(ARRAY(sa.String),default=["","",""])
	plz = sa.Column(sa.String, default="")
	rabatt = sa.Column(sa.Numeric, default=0)
	segment1 = sa.Column(sa.Integer, default=0)
	skonto = sa.Column(sa.Numeric, default=0)
	telefon = sa.Column(sa.String, default="")
	telex = sa.Column(sa.String, default="")
	vorname1 = sa.Column(sa.String, default="")
	wohnort = sa.Column(sa.String, default="")
	z_code = sa.Column(sa.String, default="")
	ziel = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
