from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kresline(Base):
	__tablename__ = 'kresline'

	anz = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	buchart = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	departement = sa.Column(sa.Integer, default=0)
	firstper = sa.Column(sa.Boolean, default=True)
	gastnr = sa.Column(sa.Integer, default=0)
	id = sa.Column(sa.String, default="")
	kabnr = sa.Column(sa.Integer, default=0)
	kreslinr = sa.Column(sa.Integer, default=0)
	kurresnr = sa.Column(sa.Integer, default=0)
	lupdate = sa.Column(sa.String, default="")
	massfest = sa.Column(sa.Boolean, default=False)
	massnr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	zeitanw = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
