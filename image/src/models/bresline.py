from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bresline(Base):
	__tablename__ = 'bresline'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bankettnr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_zeit = sa.Column(sa.String, default="")
	breslinnr = sa.Column(sa.Integer, default=0)
	briefnr = sa.Column(sa.Integer, default=0)
	buchstatus = sa.Column(sa.Boolean, default=False)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	departement = sa.Column(sa.Integer, default=0)
	fakturiert = sa.Column(sa.Integer, default=0)
	fname = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=0)
	information = sa.Column(sa.String, default="")
	limitdate = sa.Column(sa.Date, default=None)
	notizen = sa.Column(sa.String, default="")
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	r_status = sa.Column(sa.Integer, default=0)
	raum = sa.Column(sa.String, default="")
	raum_line = sa.Column(sa.Integer, default=0)
	setup = sa.Column(sa.String, default="")
	texte = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","","",""])
	typ = sa.Column(sa.String, default="")
	vname = sa.Column(sa.String, default="")
	von_equipnr = sa.Column(sa.Integer, default=0)
	von_zeit = sa.Column(sa.String, default="")
	zu_equipnr = sa.Column(sa.Integer, default=0)
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
