from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bediener(Base):
	__tablename__ = 'bediener'

	betriebsnr = sa.Column(sa.Integer, default=0)
	char1 = sa.Column(sa.String, default="")
	flag = sa.Column(sa.Integer, default=0)
	kassenbest = sa.Column(sa.Numeric, default=0)
	mapi_password = sa.Column(sa.String, default="")
	mapi_profile = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	permissions = sa.Column(sa.String, default="")
	user_group = sa.Column(sa.Integer, default=0)
	usercode = sa.Column(sa.String, default="")
	userinit = sa.Column(sa.String, default="")
	username = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
