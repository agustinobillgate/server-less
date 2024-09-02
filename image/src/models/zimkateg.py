from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zimkateg(Base):
	__tablename__ = 'zimkateg'

	active = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	global_kat = sa.Column(sa.Boolean, default=False)
	kurzbez = sa.Column(sa.String, default="")
	maxzimanz = sa.Column(sa.Integer, default=1)
	normalbeleg = sa.Column(sa.Integer, default=1)
	overbooking = sa.Column(sa.Integer, default=0)
	typ = sa.Column(sa.Integer, default=0)
	verfuegbarkeit = sa.Column(sa.Boolean, default=False)
	zibelstat = sa.Column(sa.Boolean, default=False)
	zikatnr = sa.Column(sa.Integer, default=0)
	zimanzargt = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	_recid = sa.Column(sa.Integer, primary_key=True)
