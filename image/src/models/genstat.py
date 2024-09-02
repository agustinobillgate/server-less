from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Genstat(Base):
	__tablename__ = 'genstat'

	ankflag = sa.Column(sa.Boolean, default=False)
	argt = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	domestic = sa.Column(sa.Integer, default=0)
	erwachs = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=None)
	gastnrmember = sa.Column(sa.Integer, default=0)
	gratis = sa.Column(sa.Integer, default=0)
	karteityp = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Integer, default=0)
	kind2 = sa.Column(sa.Integer, default=0)
	kind3 = sa.Column(sa.Integer, default=0)
	kontcode = sa.Column(sa.String, default="")
	logis = sa.Column(sa.Numeric, default=0)
	nationnr = sa.Column(sa.Integer, default=0)
	ratelocal = sa.Column(sa.Numeric, default=0)
	res_char = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	res_deci = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	res_logic = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	resident = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	resstatus = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	source = sa.Column(sa.Integer, default=0)
	wahrungsnr = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	zipreis = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
