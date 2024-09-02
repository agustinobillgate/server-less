from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_op(Base):
	__tablename__ = 'fa_op'

	anzahl = sa.Column(sa.Integer, default=0)
	changed = sa.Column(sa.Date, default=None)
	cid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=lambda: get_current_date())
	datum = sa.Column(sa.Date, default=None)
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	id = sa.Column(sa.String, default="")
	lief_nr = sa.Column(sa.Integer, default=0)
	loeschflag = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	opart = sa.Column(sa.Integer, default=0)
	retour_reason = sa.Column(sa.String, default="")
	sysdate = sa.Column(sa.Date, default=lambda: get_current_date())
	warenwert = sa.Column(sa.Numeric, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
