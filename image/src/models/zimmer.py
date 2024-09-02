from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zimmer(Base):
	__tablename__ = 'zimmer'

	bediener_nr_stat = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	build = sa.Column(sa.String, default="")
	code = sa.Column(sa.String, default="")
	etage = sa.Column(sa.Integer, default=0)
	features = sa.Column(sa.String, default="")
	fixpreis = sa.Column(sa.Boolean, default=False)
	flag1 = sa.Column(sa.Integer, default=0)
	flag2 = sa.Column(sa.Integer, default=0)
	flag3 = sa.Column(sa.Integer, default=0)
	flag4 = sa.Column(sa.Integer, default=0)
	himmelsr = sa.Column(sa.String, default="")
	house_status = sa.Column(sa.Integer, default=0)
	kbezeich = sa.Column(sa.String, default="")
	nebenstelle = sa.Column(sa.String, default="")
	nebstflag = sa.Column(sa.Integer, default=0)
	owner_nr = sa.Column(sa.Integer, default=0)
	personal = sa.Column(sa.Boolean, default=False)
	personen = sa.Column(sa.Integer, default=0)
	prioritaet = sa.Column(sa.Integer, default=1)
	reihenfolge = sa.Column(sa.Integer, default=0)
	setup = sa.Column(sa.Integer, default=0)
	sleeping = sa.Column(sa.Boolean, default=False)
	sollflag = sa.Column(sa.Integer, default=0)
	typ = sa.Column(sa.Integer, default=0)
	verbindung = sa.Column(ARRAY(sa.String),default=["","",""])
	vid_actuel = sa.Column(sa.Integer, default=0)
	vid_request = sa.Column(sa.Integer, default=0)
	wertigkeit = sa.Column(sa.Integer, default=1)
	zikatnr = sa.Column(sa.Integer, default=0)
	zikennz = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="1")
	zistatus = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
