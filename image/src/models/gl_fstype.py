from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gl_fstype(Base):
	__tablename__ = 'gl_fstype'

	bezeich = sa.Column(sa.String, default="")
	kurzbez = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
