from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_raum(Base):
	__tablename__ = 'bk_raum'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	bname = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	groesse = sa.Column(sa.Integer, default=0)
	lu_raum = sa.Column(sa.String, default="")
	nachlauf = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	reihenfolge = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	vorbereit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
