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
