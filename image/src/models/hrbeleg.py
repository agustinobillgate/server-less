#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hrbeleg(Base):
	__tablename__ = 'hrbeleg'

	betriebsnr = sa.Column(sa.Integer, default=0)
	couverts_eff = sa.Column(sa.Integer, default=0)
	couverts100 = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	departement = sa.Column(sa.Integer, default=0)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	hour = sa.Column(sa.Integer, default=0)
	intervall = sa.Column(sa.Integer, default=0)
	tischbel_eff = sa.Column(sa.Integer, default=0)
	tischbel100 = sa.Column(sa.Integer, default=0)
	umsatzanw = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('couverts_eff', 0)
		kwargs.setdefault('couverts100', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('hour', 0)
		kwargs.setdefault('intervall', 0)
		kwargs.setdefault('tischbel_eff', 0)
		kwargs.setdefault('tischbel100', 0)
		kwargs.setdefault('umsatzanw', 0)
		super(Hrbeleg, self).__init__(*args, **kwargs)
