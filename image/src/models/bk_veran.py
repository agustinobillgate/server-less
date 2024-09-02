from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_veran(Base):
	__tablename__ = 'bk_veran'

	activeflag = sa.Column(sa.Integer, default=0)
	anlass = sa.Column(sa.String, default="")
	art = sa.Column(sa.Integer, default=0)
	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betrag = sa.Column(sa.Numeric, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastver = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	deposit = sa.Column(sa.Numeric, default=0)
	deposit_payment = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrver = sa.Column(sa.Integer, default=0)
	infotafel = sa.Column(sa.String, default="")
	kontaktdat = sa.Column(sa.Date, default=lambda: get_current_date())
	kontaktfirst = sa.Column(sa.Date, default=None)
	kontnr_res = sa.Column(sa.Integer, default=0)
	kontnr_ver = sa.Column(sa.Integer, default=0)
	last_paid_date = sa.Column(sa.Date, default=None)
	limit_date = sa.Column(sa.Date, default=None)
	payment_date = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	payment_userinit = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	rechnr = sa.Column(sa.Integer, default=0)
	resdat = sa.Column(sa.Date, default=lambda: get_current_date())
	resnr = sa.Column(sa.Integer, default=0)
	resstatus = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	stoerung = sa.Column(sa.Boolean, default=False)
	total_paid = sa.Column(sa.Numeric, default=0)
	useridanlage = sa.Column(sa.String, default="")
	useridmutat = sa.Column(sa.String, default="")
	veran_nr = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
