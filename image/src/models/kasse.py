from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kasse(Base):
	__tablename__ = 'kasse'

	artnr = sa.Column(sa.Integer, default=0)
	betrieb_gastk = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	kadresse1 = sa.Column(sa.String, default="")
	kadresse2 = sa.Column(sa.String, default="")
	kassen_nr = sa.Column(sa.Integer, default=0)
	kassenbez = sa.Column(sa.String, default="")
	kgastnr = sa.Column(sa.Integer, default=0)
	kland = sa.Column(sa.String, default="")
	kplz = sa.Column(sa.String, default="")
	ktelefon = sa.Column(sa.String, default="")
	kwohnort = sa.Column(sa.String, default="")
	preiskat = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
