from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gentable(Base):
	__tablename__ = 'gentable'

	activeflag = sa.Column(sa.Boolean, default=True)
	char_ext = sa.Column(ARRAY(sa.String),default=["","","","","","","","",""])
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	combo_ext = sa.Column(ARRAY(sa.String),default=["","",""])
	date_ext = sa.Column(ARRAY(sa.Date),default=[None,None,None,None,None,None,None,None,None])
	date1 = sa.Column(sa.Date, default=None)
	date2 = sa.Column(sa.Date, default=None)
	date3 = sa.Column(sa.Date, default=None)
	deci_ext = sa.Column(ARRAY(sa.Numeric),default=[0,0,0,0,0,0,0,0,0])
	inte_ext = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0])
	key = sa.Column(sa.String, default="")
	logi_ext = sa.Column(ARRAY(sa.Boolean),default=[False,False,False,False,False,False,False,False,False])
	logi1 = sa.Column(sa.Boolean, default=False)
	logi2 = sa.Column(sa.Boolean, default=False)
	logi3 = sa.Column(sa.Boolean, default=False)
	number1 = sa.Column(sa.Integer, default=0)
	number2 = sa.Column(sa.Integer, default=0)
	number3 = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
