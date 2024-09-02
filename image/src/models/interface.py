from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Interface(Base):
	__tablename__ = 'interface'

	action = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	decfield = sa.Column(sa.Numeric, default=0)
	int_time = sa.Column(sa.Integer, default=0)
	intdate = sa.Column(sa.Date, default=None)
	intfield = sa.Column(sa.Integer, default=0)
	key = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	parameters = sa.Column(sa.String, default="")
	reslinnr = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="1")
	zinr_old = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
