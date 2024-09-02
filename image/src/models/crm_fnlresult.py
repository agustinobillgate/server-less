from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Crm_fnlresult(Base):
	__tablename__ = 'crm_fnlresult'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	description = sa.Column(sa.String, default="")
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	range1 = sa.Column(sa.Integer, default=0)
	range2 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
