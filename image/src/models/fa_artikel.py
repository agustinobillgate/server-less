from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_artikel(Base):
	__tablename__ = 'fa_artikel'

	anz_depn = sa.Column(sa.Integer, default=0)
	anz100 = sa.Column(sa.Integer, default=0)
	anzahl = sa.Column(sa.Integer, default=1)
	book_wert = sa.Column(sa.Numeric, default=0)
	changed = sa.Column(sa.Date, default=None)
	cid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=lambda: get_current_date())
	credit_fibu = sa.Column(sa.String, default="")
	debit_fibu = sa.Column(sa.String, default="")
	deleted = sa.Column(sa.Date, default=None)
	depn_wert = sa.Column(sa.Numeric, default=0)
	did = sa.Column(sa.String, default="")
	fibukonto = sa.Column(sa.String, default="")
	first_depn = sa.Column(sa.Date, default=None)
	gnr = sa.Column(sa.Integer, default=0)
	id = sa.Column(sa.String, default="")
	katnr = sa.Column(sa.Integer, default=0)
	last_depn = sa.Column(sa.Date, default=None)
	lief_nr = sa.Column(sa.Integer, default=0)
	loeschflag = sa.Column(sa.Integer, default=0)
	next_depn = sa.Column(sa.Date, default=None)
	nr = sa.Column(sa.Integer, default=0)
	p_nr = sa.Column(sa.Integer, default=0)
	posted = sa.Column(sa.Boolean, default=False)
	subgrp = sa.Column(sa.Integer, default=0)
	warenwert = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
