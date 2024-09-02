from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mathis(Base):
	__tablename__ = 'mathis'

	asset = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	flag = sa.Column(sa.Integer, default=0)
	fname = sa.Column(sa.String, default="")
	location = sa.Column(sa.String, default="")
	mark = sa.Column(sa.String, default="")
	model = sa.Column(sa.String, default="")
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	price = sa.Column(sa.Numeric, default=0)
	remark = sa.Column(sa.String, default="")
	spec = sa.Column(sa.String, default="")
	supplier = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
