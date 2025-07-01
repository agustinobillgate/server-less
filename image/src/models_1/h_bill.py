#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_bill(Base):
	__tablename__ = 'h_bill'

	belegung = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	billnr = sa.Column(sa.Integer, default=1)
	bilname = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	flag = sa.Column(sa.Integer, default=0)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	kellner_nr = sa.Column(sa.Integer, default=0)
	mwst = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	rechnr = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	rgdruck = sa.Column(sa.Integer, default=0)
	saldo = sa.Column(sa.Numeric, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	service = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	tischnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('belegung', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('billnr', 1)
		kwargs.setdefault('bilname', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('gesamtumsatz', 0)
		kwargs.setdefault('kellner_nr', 0)
		kwargs.setdefault('mwst', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('reslinnr', 1)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('rgdruck', 0)
		kwargs.setdefault('saldo', 0)
		kwargs.setdefault('segmentcode', 0)
		kwargs.setdefault('service', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('tischnr', 0)
		super(H_bill, self).__init__(*args, **kwargs)
