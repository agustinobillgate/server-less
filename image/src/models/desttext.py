from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Desttext(Base):
	__tablename__ = 'desttext'

	dtext = sa.Column(sa.String, default="")
	lang = sa.Column(sa.Integer, default=0)
	refcode = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
