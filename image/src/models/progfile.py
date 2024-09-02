from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Progfile(Base):
	__tablename__ = 'progfile'

	bezeich = sa.Column(sa.String, default="")
	catnr = sa.Column(sa.Integer, default=0)
	filename = sa.Column(sa.String, default="")
	password = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
