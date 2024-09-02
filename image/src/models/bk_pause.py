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
