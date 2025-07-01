#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_stat(Base):
	__tablename__ = 'bk_stat'

	bemerk = sa.Column(sa.String, default="")
	bev_rev = sa.Column(sa.Numeric, default=0)
	cancel_date = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	event_nr = sa.Column(sa.Integer, default=0)
	fb_rev = sa.Column(sa.Numeric, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	isstatus = sa.Column(sa.Integer, default=0)
	other_rev = sa.Column(sa.Numeric, default=0)
	pax = sa.Column(sa.Integer, default=0)
	reserve_dec = sa.Column(sa.Integer, default=0)
	reserve_int = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	resstatus = sa.Column(sa.Integer, default=0)
	rm_rev = sa.Column(sa.Numeric, default=0)
	room = sa.Column(sa.String, default="")
	salesid = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('bev_rev', 0)
		kwargs.setdefault('cancel_date', None)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('event_nr', 0)
		kwargs.setdefault('fb_rev', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('isstatus', 0)
		kwargs.setdefault('other_rev', 0)
		kwargs.setdefault('pax', 0)
		kwargs.setdefault('reserve_dec', 0)
		kwargs.setdefault('reserve_int', 0)
		kwargs.setdefault('reslinnr', 0)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('resstatus', 0)
		kwargs.setdefault('rm_rev', 0)
		kwargs.setdefault('room', "")
		kwargs.setdefault('salesid', "")
		super(Bk_stat, self).__init__(*args, **kwargs)
