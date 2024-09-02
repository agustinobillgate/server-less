from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Debthis(Base):
	__tablename__ = 'debthis'

	artnr = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	counter = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrmember = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	rechnr = sa.Column(sa.Integer, default=0)
	rgdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	verstat = sa.Column(sa.Integer, default=0)
	vesrcod = sa.Column(sa.String, default="")
	vesrdep = sa.Column(sa.Numeric, default=0)
	zahlkonto = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
