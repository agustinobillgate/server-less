from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_artikel(Base):
	__tablename__ = 'h_artikel'

	abbuchung = sa.Column(sa.Integer, default=0)
	activeflag = sa.Column(sa.Boolean, default=False)
	aenderwunsch = sa.Column(sa.Boolean, default=False)
	artart = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	artnrfront = sa.Column(sa.Integer, default=0)
	artnrlager = sa.Column(sa.Integer, default=0)
	artnrrezept = sa.Column(sa.Integer, default=0)
	autosaldo = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezaendern = sa.Column(sa.Boolean, default=False)
	bezeich = sa.Column(sa.String, default="")
	bondruckernr = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	departement = sa.Column(sa.Integer, default=0)
	e_gueltig = sa.Column(sa.Date, default=None)
	endkum = sa.Column(sa.Integer, default=0)
	epreis1 = sa.Column(sa.Numeric, default=0)
	epreis2 = sa.Column(sa.Numeric, default=0)
	gang = sa.Column(sa.Integer, default=0)
	lagernr = sa.Column(sa.Integer, default=0)
	mwst_code = sa.Column(sa.Integer, default=0)
	prozent = sa.Column(sa.Numeric, default=0)
	s_gueltig = sa.Column(sa.Date, default=None)
	service_code = sa.Column(sa.Integer, default=0)
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
