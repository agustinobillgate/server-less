from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Akt_kont(Base):
	__tablename__ = 'akt_kont'

	a_titel = sa.Column(sa.String, default="")
	abteilung = sa.Column(sa.String, default="")
	anrede = sa.Column(sa.String, default="")
	ausweis_art = sa.Column(sa.String, default="")
	ausweis_nr1 = sa.Column(sa.String, default="")
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	briefanrede = sa.Column(sa.String, default="")
	durchwahl = sa.Column(sa.String, default="")
	email_adr = sa.Column(sa.String, default="")
	fax = sa.Column(sa.String, default="")
	fax_privat = sa.Column(sa.String, default="")
	funktion = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=None)
	geburt_ort1 = sa.Column(sa.String, default="")
	geburtdatum1 = sa.Column(sa.Date, default=None)
	hauptkontakt = sa.Column(sa.Boolean, default=False)
	kategorie = sa.Column(sa.Integer, default=0)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	nation2 = sa.Column(sa.String, default="")
	pass_aust1 = sa.Column(sa.String, default="")
	pers_bez = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	sprachcode = sa.Column(sa.Integer, default=1)
	telefon = sa.Column(sa.String, default="")
	telefon_privat = sa.Column(sa.String, default="")
	v_titel = sa.Column(sa.String, default="")
	vorname = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
