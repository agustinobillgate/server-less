#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guest_pr(Base):
	__tablename__ = 'guest_pr'

	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	code = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=None)
	kurzbez = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('code', "")
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('kurzbez', "")
		super(Guest_pr, self).__init__(*args, **kwargs)
