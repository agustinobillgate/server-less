#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kresline(Base):
	__tablename__ = 'kresline'

	anz = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	buchart = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	departement = sa.Column(sa.Integer, default=0)
	firstper = sa.Column(sa.Boolean, default=True)
	gastnr = sa.Column(sa.Integer, default=0)
	id = sa.Column(sa.String, default="")
	kabnr = sa.Column(sa.Integer, default=0)
	kreslinr = sa.Column(sa.Integer, default=0)
	kurresnr = sa.Column(sa.Integer, default=0)
	lupdate = sa.Column(sa.String, default="")
	massfest = sa.Column(sa.Boolean, default=False)
	massnr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	zeitanw = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anz', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('buchart', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('firstper', True)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('id', "")
		kwargs.setdefault('kabnr', 0)
		kwargs.setdefault('kreslinr', 0)
		kwargs.setdefault('kurresnr', 0)
		kwargs.setdefault('lupdate', "")
		kwargs.setdefault('massfest', False)
		kwargs.setdefault('massnr', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('zeitanw', "")
		super(Kresline, self).__init__(*args, **kwargs)
