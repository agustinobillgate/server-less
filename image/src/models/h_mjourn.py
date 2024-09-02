from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_mjourn(Base):
	__tablename__ = 'h_mjourn'

	anzahl = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	bill_datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	h_artnr = sa.Column(sa.Integer, default=0)
	kellner_nr = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	request = sa.Column(sa.String, default="")
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	tischnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
