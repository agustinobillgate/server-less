from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_fsdef(Base):
	__tablename__ = 'bk_fsdef'

	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	fs_field_active = sa.Column(sa.Boolean, default=False)
	fs_field_length = sa.Column(sa.Integer, default=0)
	fs_field_name = sa.Column(sa.String, default="")
	fsname = sa.Column(sa.String, default="")
	segmentcode = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
