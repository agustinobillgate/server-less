from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Dml_art(Base):
	__tablename__ = 'dml_art'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	chginit = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	einzelpreis = sa.Column(sa.Numeric, default=0)
	geliefert = sa.Column(sa.Numeric, default=0)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
