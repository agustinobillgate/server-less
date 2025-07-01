#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_op(Base):
	__tablename__ = 'l_op'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	deci1 = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	docu_nr = sa.Column(sa.String, default="")
	einzelpreis = sa.Column(sa.Numeric, default=0)
	flag = sa.Column(sa.Boolean, default=False)
	fuellflag = sa.Column(sa.Integer, default=0)
	herkunftflag = sa.Column(sa.Integer, default=0)
	lager_nr = sa.Column(sa.Integer, default=0)
	lief_nr = sa.Column(sa.Integer, default=0)
	loeschflag = sa.Column(sa.Integer, default=0)
	lscheinnr = sa.Column(sa.String, default="")
	op_art = sa.Column(sa.Integer, default=0)
	pos = sa.Column(sa.Integer, default=0)
	reorgflag = sa.Column(sa.Integer, default=0)
	rueckgabegrund = sa.Column(sa.Integer, default=0)
	stornogrund = sa.Column(sa.String, default="")
	warenwert = sa.Column(sa.Numeric, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('deci1', [0,0,0,0])
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('einzelpreis', 0)
		kwargs.setdefault('flag', False)
		kwargs.setdefault('fuellflag', 0)
		kwargs.setdefault('herkunftflag', 0)
		kwargs.setdefault('lager_nr', 0)
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('loeschflag', 0)
		kwargs.setdefault('lscheinnr', "")
		kwargs.setdefault('op_art', 0)
		kwargs.setdefault('pos', 0)
		kwargs.setdefault('reorgflag', 0)
		kwargs.setdefault('rueckgabegrund', 0)
		kwargs.setdefault('stornogrund', "")
		kwargs.setdefault('warenwert', 0)
		kwargs.setdefault('zeit', 0)
		super(L_op, self).__init__(*args, **kwargs)
