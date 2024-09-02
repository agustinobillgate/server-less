from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class History(Base):
	__tablename__ = 'history'

	abreise = sa.Column(sa.Date, default=None)
	abreisezeit = sa.Column(sa.String, default="")
	ankunft = sa.Column(sa.Date, default=None)
	argtumsatz = sa.Column(sa.Numeric, default=0)
	arrangement = sa.Column(sa.String, default="000")
	bemerk = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	com_argt = sa.Column(sa.Numeric, default=0)
	com_f_b = sa.Column(sa.Numeric, default=0)
	com_logis = sa.Column(sa.Numeric, default=0)
	com_sonst = sa.Column(sa.Numeric, default=0)
	erwachs = sa.Column(sa.Integer, default=0)
	f_b_umsatz = sa.Column(sa.Numeric, default=0)
	gastinfo = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=0)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	gratis = sa.Column(sa.Integer, default=0)
	guestnrcom = sa.Column(sa.Integer, default=0)
	kind = sa.Column(ARRAY(sa.Integer),default=[0,0])
	logisumsatz = sa.Column(sa.Numeric, default=0)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	sonst_umsatz = sa.Column(sa.Numeric, default=0)
	ums_kurz = sa.Column(sa.Numeric, default=0)
	ums_lang = sa.Column(sa.Numeric, default=0)
	zahlungsart = sa.Column(sa.Integer, default=0)
	zi_wechsel = sa.Column(sa.Boolean, default=False)
	zikateg = sa.Column(sa.String, default="")
	zimmeranz = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	zipreis = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
