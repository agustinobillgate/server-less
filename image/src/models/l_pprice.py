from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_pprice(Base):
	__tablename__ = 'l_pprice'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bestelldatum = sa.Column(sa.Date, default=lambda: get_current_date())
	betriebsnr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	lief_nr = sa.Column(sa.Integer, default=0)
	warenwert = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
