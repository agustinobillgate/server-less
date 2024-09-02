from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_rset(Base):
	__tablename__ = 'bk_rset'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	bname = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	groesse = sa.Column(sa.Integer, default=0)
	nachlauf = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	rset_nr = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	setup_id = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	vorbereit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
