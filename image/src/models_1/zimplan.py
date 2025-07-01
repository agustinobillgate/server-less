#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zimplan(Base):
	__tablename__ = 'zimplan'

	ankunft = sa.Column(sa.Date, default=get_current_date())
	bemerk = sa.Column(sa.String, default="")
	betrieb_gastmem = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	gastnrmember = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	res_recid = sa.Column(sa.Integer, default=0)
	res_recid2 = sa.Column(sa.Integer, default=0)
	res_rowid = sa.Column(sa.String, default="")
	resstatus = sa.Column(sa.Integer, default=1)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('ankunft', get_current_date())
		kwargs.setdefault('bemerk', "")
		kwargs.setdefault('betrieb_gastmem', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('datum', None)
		kwargs.setdefault('gastnrmember', 0)
		kwargs.setdefault('name', "")
		kwargs.setdefault('res_recid', 0)
		kwargs.setdefault('res_recid2', 0)
		kwargs.setdefault('res_rowid', "")
		kwargs.setdefault('resstatus', 1)
		kwargs.setdefault('zinr', "")
		super(Zimplan, self).__init__(*args, **kwargs)
