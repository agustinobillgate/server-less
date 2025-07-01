#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_orderhdr(Base):
	__tablename__ = 'l_orderhdr'

	angebot_lief = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	bestellart = sa.Column(sa.String, default="")
	bestelldatum = sa.Column(sa.Date, default=get_current_date())
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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('angebot_lief', [0,0,0])
		kwargs.setdefault('bestellart', "")
		kwargs.setdefault('bestelldatum', get_current_date())
		kwargs.setdefault('besteller', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('gedruckt', None)
		kwargs.setdefault('gefaxt', None)
		kwargs.setdefault('lief_fax', ["","",""])
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('lieferdatum', None)
		kwargs.setdefault('txtnr', None)
		super(L_orderhdr, self).__init__(*args, **kwargs)
