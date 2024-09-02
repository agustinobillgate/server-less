from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_artikel(Base):
	__tablename__ = 'l_artikel'

	alkoholgrad = sa.Column(sa.Numeric, default=0)
	anzverbrauch = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bestellt = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	ek_aktuell = sa.Column(sa.Numeric, default=0)
	ek_letzter = sa.Column(sa.Numeric, default=0)
	endkum = sa.Column(sa.Integer, default=0)
	erfass_art = sa.Column(sa.Boolean, default=False)
	fibukonto = sa.Column(sa.String, default="")
	herkunft = sa.Column(sa.String, default="")
	inhalt = sa.Column(sa.Numeric, default=1)
	jahrgang = sa.Column(sa.Integer, default=0)
	letz_ausgang = sa.Column(sa.Date, default=None)
	letz_eingang = sa.Column(sa.Date, default=None)
	lief_artnr = sa.Column(ARRAY(sa.String),default=["","",""])
	lief_einheit = sa.Column(sa.Numeric, default=1)
	lief_nr1 = sa.Column(sa.Integer, default=0)
	lief_nr2 = sa.Column(sa.Integer, default=0)
	lief_nr3 = sa.Column(sa.Integer, default=0)
	lieferfrist = sa.Column(sa.Integer, default=0)
	masseinheit = sa.Column(sa.String, default="")
	min_bestand = sa.Column(sa.Numeric, default=0)
	traubensorte = sa.Column(sa.String, default="")
	vk_preis = sa.Column(sa.Numeric, default=0)
	wert_verbrau = sa.Column(sa.Numeric, default=0)
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
