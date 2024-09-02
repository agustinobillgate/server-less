from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Ba_setup(Base):
	__tablename__ = 'ba_setup'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeichnung = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	segmentcode = sa.Column(sa.Integer, default=0)
	setup_id = sa.Column(sa.Integer, default=0)
	vname = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
