#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_pause(Base):
	__tablename__ = 'bk_pause'

	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_datum = sa.Column(sa.Date, default=None)
	bis_i = sa.Column(sa.Integer, default=0)
	bis_zeit = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	p_nr = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	veran_nr = sa.Column(sa.Integer, default=0)
	veran_resnr = sa.Column(sa.Integer, default=0)
	veran_seite = sa.Column(sa.Integer, default=0)
	von_i = sa.Column(sa.Integer, default=0)
	von_zeit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('bemerkung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bis_datum', None)
		kwargs.setdefault('bis_i', 0)
		kwargs.setdefault('bis_zeit', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('p_nr', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('veran_nr', 0)
		kwargs.setdefault('veran_resnr', 0)
		kwargs.setdefault('veran_seite', 0)
		kwargs.setdefault('von_i', 0)
		kwargs.setdefault('von_zeit', "")
		super(Bk_pause, self).__init__(*args, **kwargs)
