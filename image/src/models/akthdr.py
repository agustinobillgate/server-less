from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Akthdr(Base):
	__tablename__ = 'akthdr'

	aktnr = sa.Column(sa.Integer, default=0)
	amount = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	bemerk = sa.Column(sa.String, default="")
	bezeich = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	chg_datum = sa.Column(sa.Date, default=lambda: get_current_date())
	chg_id = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	dec1 = sa.Column(sa.Numeric, default=0)
	dec2 = sa.Column(sa.Numeric, default=0)
	dec3 = sa.Column(sa.Numeric, default=0)
	erl_datum = sa.Column(sa.Date, default=None)
	erledigt = sa.Column(sa.Boolean, default=False)
	flag = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	grund = sa.Column(sa.Integer, default=0)
	int1 = sa.Column(sa.Integer, default=0)
	int2 = sa.Column(sa.Integer, default=0)
	int3 = sa.Column(sa.Integer, default=0)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	mitbewerber = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	next_datum = sa.Column(sa.Date, default=None)
	next_zeit = sa.Column(sa.Integer, default=0)
	prioritaet = sa.Column(sa.Integer, default=0)
	product = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	prozent = sa.Column(sa.Integer, default=0)
	referred = sa.Column(sa.Integer, default=0)
	stichwort = sa.Column(sa.String, default="")
	stufe = sa.Column(sa.Integer, default=0)
	t_betrag = sa.Column(sa.Numeric, default=0)
	userinit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
