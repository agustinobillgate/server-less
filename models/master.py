#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Master(Base):
	__tablename__ = 'master'

	active = sa.Column(sa.Boolean, default=False)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betrieb_gastpay = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	flag = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	gastnrpay = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	rechnr = sa.Column(sa.Integer, default=0)
	rechnrend = sa.Column(sa.Integer, default=0)
	rechnrstart = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	umsatzart = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False])
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('active', False)
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betrieb_gastpay', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('gastnrpay', 0)
		kwargs.setdefault('name', "")
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('rechnrend', 0)
		kwargs.setdefault('rechnrstart', 0)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('umsatzart', [False,False,False,False])
		super(Master, self).__init__(*args, **kwargs)
