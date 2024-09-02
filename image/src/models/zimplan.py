from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zimplan(Base):
	__tablename__ = 'zimplan'

	ankunft = sa.Column(sa.Date, default=lambda: get_current_date())
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
