from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kontline(Base):
	__tablename__ = 'kontline'

	abreise = sa.Column(sa.Date, default=None)
	adrflag = sa.Column(sa.Boolean, default=False)
	ankunft = sa.Column(sa.Date, default=lambda: get_current_date())
	ankzeit = sa.Column(sa.Integer, default=0)
	ansprech = sa.Column(sa.String, default="")
	anztage = sa.Column(sa.Integer, default=1)
	arrangement = sa.Column(sa.String, default="")
	bediener_nr = sa.Column(sa.Integer, default=0)
	bemerk = sa.Column(sa.String, default="")
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastpay = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	code = sa.Column(sa.String, default="")
	day_setting = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0])
	erwachs = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrpay = sa.Column(sa.Integer, default=0)
	gratis = sa.Column(sa.Integer, default=0)
	kind1 = sa.Column(sa.Integer, default=0)
	kind2 = sa.Column(sa.Integer, default=0)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	kontcode = sa.Column(sa.String, default="")
	kontignr = sa.Column(sa.Integer, default=0)
	kontstatus = sa.Column(sa.Integer, default=1)
	overbooking = sa.Column(sa.Integer, default=0)
	pr_code = sa.Column(sa.String, default="")
	resdat = sa.Column(sa.Date, default=lambda: get_current_date())
	rueckdatum = sa.Column(sa.Date, default=None)
	ruecktage = sa.Column(sa.Integer, default=0)
	useridanlage = sa.Column(sa.String, default="")
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=1)
	zipreis = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
