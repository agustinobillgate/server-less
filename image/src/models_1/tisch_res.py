#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Tisch_res(Base):
	__tablename__ = 'tisch_res'

	bemerk = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_dat = sa.Column(sa.Date, default=None)
	bis_zeit = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	departement = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	name = sa.Column(sa.String, default="")
	number1 = sa.Column(sa.Integer, default=0)
	persanz = sa.Column(sa.Integer, default=1)
	raum = sa.Column(sa.String, default="")
	resnr = sa.Column(sa.Integer, default=0)
	tischnr = sa.Column(sa.Integer, default=0)
	von_dat = sa.Column(sa.Date, default=None)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bis_dat', None)
		kwargs.setdefault('bis_zeit', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('deci1', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('logi1', False)
		kwargs.setdefault('name', "")
		kwargs.setdefault('number1', 0)
		kwargs.setdefault('persanz', 1)
		kwargs.setdefault('raum', "")
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('tischnr', 0)
		kwargs.setdefault('von_dat', None)
		kwargs.setdefault('zeit', 0)
		kwargs.setdefault('zinr', "")
		super(Tisch_res, self).__init__(*args, **kwargs)
