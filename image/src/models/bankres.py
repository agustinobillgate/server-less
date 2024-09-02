from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bankres(Base):
	__tablename__ = 'bankres'

	activeflag = sa.Column(sa.Integer, default=0)
	anlass = sa.Column(sa.String, default="")
	bankettnr = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betrag = sa.Column(sa.Numeric, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastres = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	durchgehend = sa.Column(sa.Boolean, default=False)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrres = sa.Column(sa.Integer, default=0)
	kontaktdat = sa.Column(sa.Date, default=lambda: get_current_date())
	kontaktfirst = sa.Column(sa.Date, default=None)
	kontnr_res = sa.Column(sa.Integer, default=0)
	kontnr_ver = sa.Column(sa.Integer, default=0)
	notizen = sa.Column(ARRAY(sa.String),default=["","","","",""])
	rechnr = sa.Column(sa.Integer, default=0)
	resdat = sa.Column(sa.Date, default=lambda: get_current_date())
	stoerung = sa.Column(sa.Boolean, default=False)
	tafel = sa.Column(sa.String, default="")
	useridanlage = sa.Column(sa.String, default="")
	useridmutat = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
