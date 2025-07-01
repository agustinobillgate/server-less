#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fbstat(Base):
	__tablename__ = 'fbstat'

	bev_gcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	bev_gpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	bev_grev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	bev_wcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	bev_wpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	bev_wrev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	datum = sa.Column(sa.Date, default=None)
	departement = sa.Column(sa.Integer, default=0)
	food_gcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	food_gpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	food_grev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	food_wcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	food_wpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	food_wrev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	other_gcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	other_gpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	other_grev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	other_wcost = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	other_wpax = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0])
	other_wrev = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0])
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bev_gcost', [0,0,0,0])
		kwargs.setdefault('bev_gpax', [0,0,0,0])
		kwargs.setdefault('bev_grev', [0,0,0,0])
		kwargs.setdefault('bev_wcost', [0,0,0,0])
		kwargs.setdefault('bev_wpax', [0,0,0,0])
		kwargs.setdefault('bev_wrev', [0,0,0,0])
		kwargs.setdefault('datum', None)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('food_gcost', [0,0,0,0])
		kwargs.setdefault('food_gpax', [0,0,0,0])
		kwargs.setdefault('food_grev', [0,0,0,0])
		kwargs.setdefault('food_wcost', [0,0,0,0])
		kwargs.setdefault('food_wpax', [0,0,0,0])
		kwargs.setdefault('food_wrev', [0,0,0,0])
		kwargs.setdefault('other_gcost', [0,0,0,0])
		kwargs.setdefault('other_gpax', [0,0,0,0])
		kwargs.setdefault('other_grev', [0,0,0,0])
		kwargs.setdefault('other_wcost', [0,0,0,0])
		kwargs.setdefault('other_wpax', [0,0,0,0])
		kwargs.setdefault('other_wrev', [0,0,0,0])
		super(Fbstat, self).__init__(*args, **kwargs)
