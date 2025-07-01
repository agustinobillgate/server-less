#version: 1.0.0.3

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('char1', "")
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('kassenbest', 0)
		kwargs.setdefault('mapi_password', "")
		kwargs.setdefault('mapi_profile', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('permissions', "")
		kwargs.setdefault('user_group', 0)
		kwargs.setdefault('usercode', "")
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('username', "")
		super(Bediener, self).__init__(*args, **kwargs)
