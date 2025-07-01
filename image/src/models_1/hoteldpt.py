#version: 1.0.0.2

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bankettfsnr', 0)
		kwargs.setdefault('bankettp2', "")
		kwargs.setdefault('bankettp3', "")
		kwargs.setdefault('bankettp4', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('defult', False)
		kwargs.setdefault('depart', "")
		kwargs.setdefault('departtyp', 0)
		kwargs.setdefault('konto_nr', "")
		kwargs.setdefault('num', 0)
		kwargs.setdefault('tagungfsnr', 0)
		kwargs.setdefault('tagungp2', "")
		kwargs.setdefault('tagungp3', "")
		kwargs.setdefault('tagungp4', "")
		super(Hoteldpt, self).__init__(*args, **kwargs)
