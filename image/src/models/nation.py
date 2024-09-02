from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nation(Base):
	__tablename__ = 'nation'

	bezeich = sa.Column(sa.String, default="")
	hauptgruppe = sa.Column(sa.Integer, default=1)
	in_stat = sa.Column(sa.Boolean, default=False)
	kurzbez = sa.Column(sa.String, default="")
	language = sa.Column(sa.Integer, default=0)
	natcode = sa.Column(sa.Integer, default=0)
	nationnr = sa.Column(sa.Integer, default=0)
	untergruppe = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
