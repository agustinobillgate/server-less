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
