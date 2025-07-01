#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Brief(Base):
	__tablename__ = 'brief'

	betriebsnr = sa.Column(sa.Integer, default=0)
	briefbezeich = sa.Column(sa.String, default="")
	briefkateg = sa.Column(sa.Integer, default=1)
	briefnr = sa.Column(sa.Integer, default=0)
	etk_anzahl = sa.Column(sa.Integer, default=None)
	fname = sa.Column(sa.String, default="")
	ftyp = sa.Column(sa.Integer, default=0)
	sprachcode = sa.Column(sa.Integer, default=1)
	tabulator = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('briefbezeich', "")
		kwargs.setdefault('briefkateg', 1)
		kwargs.setdefault('briefnr', 0)
		kwargs.setdefault('etk_anzahl', None)
		kwargs.setdefault('fname', "")
		kwargs.setdefault('ftyp', 0)
		kwargs.setdefault('sprachcode', 1)
		kwargs.setdefault('tabulator', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		super(Brief, self).__init__(*args, **kwargs)
