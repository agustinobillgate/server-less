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
