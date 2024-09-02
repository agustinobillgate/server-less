from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_order(Base):
	__tablename__ = 'l_order'

	angebot_lief = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bestellart = sa.Column(sa.String, default="")
	bestelldatum = sa.Column(sa.Date, default=lambda: get_current_date())
	besteller = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	flag = sa.Column(sa.Boolean, default=False)
	gedruckt = sa.Column(sa.Date, default=None)
	gefaxt = sa.Column(sa.Date, default=None)
	geliefert = sa.Column(sa.Numeric, default=0)
	herkunftflag = sa.Column(sa.Integer, default=0)
	lager_nr = sa.Column(sa.Integer, default=0)
	lief_fax = sa.Column(ARRAY(sa.String),default=["","",""])
	lief_nr = sa.Column(sa.Integer, default=0)
	lieferdatum = sa.Column(sa.Date, default=None)
	lieferdatum_eff = sa.Column(sa.Date, default=None)
	loeschflag = sa.Column(sa.Integer, default=0)
	op_art = sa.Column(sa.Integer, default=0)
	pos = sa.Column(sa.Integer, default=0)
	quality = sa.Column(sa.String, default="")
	rechnungspreis = sa.Column(sa.Numeric, default=0)
	rechnungswert = sa.Column(sa.Numeric, default=0)
	rueckgabegrund = sa.Column(sa.Integer, default=0)
	stornogrund = sa.Column(sa.String, default="")
	txtnr = sa.Column(sa.Integer, default=1)
	warenwert = sa.Column(sa.Numeric, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
