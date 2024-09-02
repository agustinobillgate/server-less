from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Telephone(Base):
	__tablename__ = 'telephone'

	adresse1 = sa.Column(sa.String, default="")
	adresse2 = sa.Column(sa.String, default="")
	anrede = sa.Column(sa.String, default="")
	bediener_nr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	dept = sa.Column(sa.String, default="")
	ext = sa.Column(sa.String, default="")
	fax = sa.Column(sa.String, default="")
	fax_ext = sa.Column(sa.String, default="")
	fax_prefix = sa.Column(sa.String, default="")
	land = sa.Column(sa.String, default="")
	land_code = sa.Column(sa.String, default="")
	mobil_prefix = sa.Column(sa.String, default="")
	mobil_telefon = sa.Column(sa.String, default="")
	name = sa.Column(sa.String, default="")
	prefix = sa.Column(sa.String, default="")
	privat_prefix = sa.Column(sa.String, default="")
	telefon_privat = sa.Column(sa.String, default="")
	telephone = sa.Column(sa.String, default="")
	telex = sa.Column(sa.String, default="")
	telex_ext = sa.Column(sa.String, default="")
	telex_prefix = sa.Column(sa.String, default="")
	vorname = sa.Column(sa.String, default="")
	wohnort = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
