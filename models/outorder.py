#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Outorder(Base):
	__tablename__ = 'outorder'

	betriebsnr = sa.Column(sa.Integer, default=0)
	gespende = sa.Column(sa.Date, default=None)
	gespgrund = sa.Column(sa.String, default="")
	gespstart = sa.Column(sa.Date, default=None)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('gespende', None)
		kwargs.setdefault('gespgrund', "")
		kwargs.setdefault('gespstart', None)
		kwargs.setdefault('zinr', "")
		super(Outorder, self).__init__(*args, **kwargs)
