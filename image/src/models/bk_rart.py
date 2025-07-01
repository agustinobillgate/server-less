#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_rart(Base):
	__tablename__ = 'bk_rart'

	anzahl = sa.Column(sa.Integer, default=0)
	anzeigen = sa.Column(sa.Boolean, default=True)
	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	buchstatus = sa.Column(sa.Boolean, default=False)
	departement = sa.Column(sa.Integer, default=0)
	fakturiert = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	resstatus = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	setup = sa.Column(sa.String, default="")
	setup_id = sa.Column(sa.Integer, default=0)
	standardequipment = sa.Column(sa.Boolean, default=False)
	veran_artnr = sa.Column(sa.Integer, default=0)
	veran_nr = sa.Column(sa.Integer, default=0)
	veran_resnr = sa.Column(sa.Integer, default=0)
	veran_seite = sa.Column(sa.Integer, default=0)
	veran_typ = sa.Column(sa.Integer, default=0)
	von_zeit = sa.Column(sa.String, default="")
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('anzeigen', True)
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('buchstatus', False)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('fakturiert', 0)
		kwargs.setdefault('preis', 0)
		kwargs.setdefault('raum', "")
		kwargs.setdefault('resstatus', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('setup', "")
		kwargs.setdefault('setup_id', 0)
		kwargs.setdefault('standardequipment', False)
		kwargs.setdefault('veran_artnr', 0)
		kwargs.setdefault('veran_nr', 0)
		kwargs.setdefault('veran_resnr', 0)
		kwargs.setdefault('veran_seite', 0)
		kwargs.setdefault('veran_typ', 0)
		kwargs.setdefault('von_zeit', "")
		kwargs.setdefault('zwkum', 0)
		super(Bk_rart, self).__init__(*args, **kwargs)
