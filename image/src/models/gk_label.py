from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gk_label(Base):
	__tablename__ = 'gk_label'

	betriebsnr = sa.Column(sa.Integer, default=0)
	display_help = sa.Column(sa.String, default="")
	display_name = sa.Column(sa.String, default="")
	field_help = sa.Column(sa.String, default="")
	field_label = sa.Column(sa.String, default="")
	field_name = sa.Column(sa.String, default=None)
	karteityp = sa.Column(sa.Integer, default=0)
	language = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
