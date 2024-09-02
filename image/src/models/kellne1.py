from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kellne1(Base):
	__tablename__ = 'kellne1'

	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	kellner_nr = sa.Column(sa.Integer, default=1)
	kumsatz_nr = sa.Column(sa.Integer, default=0)
	kzahl_nr = sa.Column(sa.Integer, default=0)
	saldo = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
