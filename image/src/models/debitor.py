from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Debitor(Base):
	__tablename__ = 'debitor'

	artnr = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastmem = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	debref = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrmember = sa.Column(sa.Integer, default=0)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	mahnstufe = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	opart = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	rgdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	transzeit = sa.Column(sa.Integer, default=0)
	versanddat = sa.Column(sa.Date, default=None)
	verstat = sa.Column(sa.Integer, default=0)
	vesrcod = sa.Column(sa.String, default="")
	vesrdat = sa.Column(sa.Date, default=None)
	vesrdep = sa.Column(sa.Numeric, default=0)
	vesrdepot = sa.Column(sa.String, default="")
	vesrdepot2 = sa.Column(sa.String, default="")
	zahlkonto = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
