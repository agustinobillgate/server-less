from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Eg_staff(Base):
	__tablename__ = 'eg_staff'

	activeflag = sa.Column(sa.Boolean, default=False)
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	mobile = sa.Column(sa.String, default="")
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	position = sa.Column(sa.String, default="")
	remarks = sa.Column(sa.String, default="")
	skill = sa.Column(sa.String, default="")
	usergroup = sa.Column(sa.Integer, default=0)
	vhpuser = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
