from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Htparam(Base):
	__tablename__ = 'htparam'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	fchar = sa.Column(sa.String, default="")
	fdate = sa.Column(sa.Date, default=None)
	fdecimal = sa.Column(sa.Numeric, default=0)
	fdefault = sa.Column(sa.String, default="")
	feldtyp = sa.Column(sa.Integer, default=0)
	finteger = sa.Column(sa.Integer, default=0)
	flogical = sa.Column(sa.Boolean, default=False)
	htp_help = sa.Column(sa.String, default="")
	lupdate = sa.Column(sa.Date, default=lambda: get_current_date())
	paramgruppe = sa.Column(sa.Integer, default=0)
	paramnr = sa.Column(sa.Integer, default=0)
	reihenfolge = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)


