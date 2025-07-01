#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zkstat(Base):
	__tablename__ = 'zkstat'

	anz_abr = sa.Column(sa.Integer, default=0)
	anz_ankunft = sa.Column(sa.Integer, default=0)
	anz100 = sa.Column(sa.Integer, default=0)
	anz100argtart = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	arrangement_art = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	personen = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anz_abr', 0)
		kwargs.setdefault('anz_ankunft', 0)
		kwargs.setdefault('anz100', 0)
		kwargs.setdefault('anz100argtart', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('arrangement_art', [0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('personen', 0)
		kwargs.setdefault('zikatnr', 0)
		kwargs.setdefault('zimmeranz', 0)
		super(Zkstat, self).__init__(*args, **kwargs)
