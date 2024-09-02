from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sourccod(Base):
	__tablename__ = 'sourccod'

	bemerkung = sa.Column(sa.String, default="")
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	source_code = sa.Column(sa.Integer, default=0)
	sourcegrup = sa.Column(sa.Integer, default=1)
	vip_level = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
