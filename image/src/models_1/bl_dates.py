#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bl_dates(Base):
	__tablename__ = 'bl_dates'

	betriebsnr = sa.Column(sa.Integer, default=0)
	gespende = sa.Column(sa.Date, default=None)
	gespgrund = sa.Column(sa.String, default="")
	gespstart = sa.Column(sa.Date, default=None)
	user_group = sa.Column(sa.Integer, default=0)
	zikatnr = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('gespende', None)
		kwargs.setdefault('gespgrund', "")
		kwargs.setdefault('gespstart', None)
		kwargs.setdefault('user_group', 0)
		kwargs.setdefault('zikatnr', 0)
		kwargs.setdefault('zimmeranz', 1)
		super(Bl_dates, self).__init__(*args, **kwargs)
