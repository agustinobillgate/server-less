from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Briefzei(Base):
	__tablename__ = 'briefzei'

	betriebsnr = sa.Column(sa.Integer, default=0)
	briefnr = sa.Column(sa.Integer, default=0)
	briefzeilnr = sa.Column(sa.Integer, default=0)
	texte = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
