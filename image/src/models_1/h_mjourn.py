#version: 1.0.0.2

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
	sysdate = sa.Column(sa.Date, default=get_current_date())
	tischnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('bill_datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('h_artnr', 0)
		kwargs.setdefault('kellner_nr', 0)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('request', "")
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('tischnr', 0)
		kwargs.setdefault('zeit', 0)
		super(H_mjourn, self).__init__(*args, **kwargs)
