from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_histtrain(Base):
	__tablename__ = 'cl_histtrain'

	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	class_ = sa.Column('class', sa.Integer)
	codenum = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	deci2 = sa.Column(sa.Numeric, default=0)
	deci3 = sa.Column(sa.Numeric, default=0)
	endtime = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	remain = sa.Column(sa.Integer, default=0)
	remarks = sa.Column(sa.String, default="")
	reslinnr = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	starttime = sa.Column(sa.Integer, default=0)
	trainer = sa.Column(sa.Integer, default=0)
	voucherno = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
