#version: 1.0.0.2

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
	rgdatum = sa.Column(sa.Date, default=get_current_date())
	saldo = sa.Column(sa.Numeric, default=0)
	verstat = sa.Column(sa.Integer, default=0)
	vesrcod = sa.Column(sa.String, default="")
	vesrdep = sa.Column(sa.Numeric, default=0)
	zahlkonto = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('counter', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('gastnrmember', 0)
		kwargs.setdefault('name', "")
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('rgdatum', get_current_date())
		kwargs.setdefault('saldo', 0)
		kwargs.setdefault('verstat', 0)
		kwargs.setdefault('vesrcod', "")
		kwargs.setdefault('vesrdep', 0)
		kwargs.setdefault('zahlkonto', 0)
		kwargs.setdefault('zinr', "")
		super(Debthis, self).__init__(*args, **kwargs)
