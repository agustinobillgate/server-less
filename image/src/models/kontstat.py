from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kontstat(Base):
	__tablename__ = 'kontstat'

	arrangement = sa.Column(sa.String, default="")
	belegt = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	erwachs = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Integer, default=0)
	kontcode = sa.Column(sa.String, default="")
	overbook = sa.Column(sa.Integer, default=0)
	personen = sa.Column(sa.Integer, default=0)
	reserve_char = sa.Column(ARRAY(sa.String),default=["","",""])
	reserve_dec = sa.Column(ARRAY(sa.Numeric),default=[0,0,0])
	reserve_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
