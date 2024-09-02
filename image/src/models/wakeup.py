from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Wakeup(Base):
	__tablename__ = 'wakeup'

	bediener_nr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	language = sa.Column(sa.Integer, default=0)
	language_code = sa.Column(sa.String, default="")
	moddatum = sa.Column(sa.Date, default=lambda: get_current_date())
	moduser = sa.Column(sa.Integer, default=0)
	modzeit = sa.Column(sa.Integer, default=0)
	usre = sa.Column(sa.String, default="")
	wakeupdone = sa.Column(sa.Integer, default=0)
	weckdatum = sa.Column(sa.Date, default=lambda: get_current_date())
	weckzeit = sa.Column(sa.String, default="")
	weckzeit_int = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
