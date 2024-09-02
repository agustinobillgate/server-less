from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_reser(Base):
	__tablename__ = 'bk_reser'

	arrangement = sa.Column(sa.String, default="")
	art_res = sa.Column(sa.Boolean, default=False)
	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_datum = sa.Column(sa.Date, default=None)
	bis_i = sa.Column(sa.Integer, default=0)
	bis_zeit = sa.Column(sa.String, default="")
	briefnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	dekoration = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	fakturiert = sa.Column(sa.Integer, default=0)
	fname = sa.Column(sa.String, default="")
	gruppenname = sa.Column(sa.String, default="")
	limitdate = sa.Column(sa.Date, default=None)
	nachlaufzeit = sa.Column(sa.Integer, default=0)
	notizen = sa.Column(sa.String, default="")
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	resstatus = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	setup = sa.Column(sa.String, default="")
	setup_id = sa.Column(sa.Integer, default=0)
	typ = sa.Column(sa.String, default="")
	veran_artnr = sa.Column(sa.Integer, default=0)
	veran_nr = sa.Column(sa.Integer, default=0)
	veran_resnr = sa.Column(sa.Integer, default=0)
	veran_seite = sa.Column(sa.Integer, default=0)
	veran_typ = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	von_i = sa.Column(sa.Integer, default=0)
	von_zeit = sa.Column(sa.String, default="")
	vorbereitungszeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
