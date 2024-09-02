from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hoteldpt(Base):
	__tablename__ = 'hoteldpt'

	bankettfsnr = sa.Column(sa.Integer, default=0)
	bankettp2 = sa.Column(sa.String, default="")
	bankettp3 = sa.Column(sa.String, default="")
	bankettp4 = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	defult = sa.Column(sa.Boolean, default=False)
	depart = sa.Column(sa.String, default="")
	departtyp = sa.Column(sa.Integer, default=0)
	konto_nr = sa.Column(sa.String, default="")
	num = sa.Column(sa.Integer, default=0)
	tagungfsnr = sa.Column(sa.Integer, default=0)
	tagungp2 = sa.Column(sa.String, default="")
	tagungp3 = sa.Column(sa.String, default="")
	tagungp4 = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
