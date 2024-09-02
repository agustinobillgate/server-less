from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_op(Base):
	__tablename__ = 'l_op'

	anzahl = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
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
