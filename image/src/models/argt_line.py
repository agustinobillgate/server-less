from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Argt_line(Base):
	__tablename__ = 'argt_line'

	argt_artnr = sa.Column(sa.Integer, default=0)
	argtnr = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	erwachs = sa.Column(sa.Boolean, default=False)
	fakt_modus = sa.Column(sa.Integer, default=1)
	gratis = sa.Column(sa.Boolean, default=True)
	intervall = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Boolean, default=False)
	kind2 = sa.Column(sa.Boolean, default=False)
	vt_percnt = sa.Column(sa.Numeric, default=0.00)
	_recid = sa.Column(sa.Integer, primary_key=True)
