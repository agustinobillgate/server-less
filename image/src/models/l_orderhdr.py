from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_orderhdr(Base):
	__tablename__ = 'l_orderhdr'

	angebot_lief = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	bestellart = sa.Column(sa.String, default="")
	bestelldatum = sa.Column(sa.Date, default=lambda: get_current_date())
	besteller = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	docu_nr = sa.Column(sa.String, default="")
	gedruckt = sa.Column(sa.Date, default=None)
	gefaxt = sa.Column(sa.Date, default=None)
	lief_fax = sa.Column(ARRAY(sa.String),default=["","",""])
	lief_nr = sa.Column(sa.Integer, default=0)
	lieferdatum = sa.Column(sa.Date, default=None)
	txtnr = sa.Column(sa.Integer, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
