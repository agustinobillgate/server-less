#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Res_history(Base):
	__tablename__ = 'res_history'

	action = sa.Column(sa.String, default="")
	aenderung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	nr = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('action', "")
		kwargs.setdefault('aenderung', "")
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('reslinnr', 1)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('zeit', 0)
		super(Res_history, self).__init__(*args, **kwargs)
