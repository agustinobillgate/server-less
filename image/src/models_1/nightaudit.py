#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nightaudit(Base):
	__tablename__ = 'nightaudit'

	abschlussart = sa.Column(sa.Boolean, default=False)
	anzkopien = sa.Column(sa.Integer, default=1)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	dekade = sa.Column(sa.Integer, default=0)
	hogarest = sa.Column(sa.Integer, default=0)
	lastrun = sa.Column(sa.Date, default=None)
	programm = sa.Column(sa.String, default="")
	reihenfolge = sa.Column(sa.Integer, default=0)
	reportnr = sa.Column(sa.Integer, default=0)
	selektion = sa.Column(sa.Boolean, default=False)
	sequenz = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('abschlussart', False)
		kwargs.setdefault('anzkopien', 1)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeichnung', "")
		kwargs.setdefault('dekade', 0)
		kwargs.setdefault('hogarest', 0)
		kwargs.setdefault('lastrun', None)
		kwargs.setdefault('programm', "")
		kwargs.setdefault('reihenfolge', 0)
		kwargs.setdefault('reportnr', 0)
		kwargs.setdefault('selektion', False)
		kwargs.setdefault('sequenz', 1)
		super(Nightaudit, self).__init__(*args, **kwargs)
