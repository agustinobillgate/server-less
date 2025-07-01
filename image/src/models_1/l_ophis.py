#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_ophis(Base):
	__tablename__ = 'l_ophis'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	fibukonto = sa.Column(sa.String, default="")
	lager_nr = sa.Column(sa.Integer, default=0)
	lief_nr = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	op_art = sa.Column(sa.Integer, default=0)
	warenwert = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('einzelpreis', 0)
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('lager_nr', 0)
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('lscheinnr', "")
		kwargs.setdefault('op_art', 0)
		kwargs.setdefault('warenwert', 0)
		super(L_ophis, self).__init__(*args, **kwargs)
