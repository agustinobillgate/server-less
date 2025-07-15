#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_op(Base):
	__tablename__ = 'fa_op'

	anzahl = sa.Column(sa.Integer, default=0)
	changed = sa.Column(sa.Date, default=None)
	cid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=get_current_date())
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
	sysdate = sa.Column(sa.Date, default=get_current_date())
	warenwert = sa.Column(sa.Numeric, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('changed', None)
		kwargs.setdefault('cid', "")
		kwargs.setdefault('created', get_current_date())
		kwargs.setdefault('datum', None)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('einzelpreis', 0)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('id', "")
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('loeschflag', 0)
		kwargs.setdefault('lscheinnr', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('opart', 0)
		kwargs.setdefault('retour_reason', "")
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('warenwert', 0)
		kwargs.setdefault('zeit', 0)
		super(Fa_op, self).__init__(*args, **kwargs)
