from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Masseur(Base):
	__tablename__ = 'masseur'

	commission = sa.Column(sa.Numeric, default=0)
	dayoff = sa.Column(sa.Boolean, default=False)
	fdate = sa.Column(sa.Date, default=None)
	grund = sa.Column(sa.String, default="")
	massnr = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	oooab = sa.Column(sa.String, default="00:00")
	ooobis = sa.Column(sa.String, default="00:00")
	pausebeg = sa.Column(sa.String, default="00:00")
	pauseend = sa.Column(sa.String, default="00:00")
	sex = sa.Column(sa.Boolean, default=False)
	tdate = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
