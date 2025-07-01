#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_home(Base):
	__tablename__ = 'cl_home'

	adresse1 = sa.Column(sa.String, default="")
	adresse2 = sa.Column(sa.String, default="")
	banner = sa.Column(sa.String, default="")
	cflag = sa.Column(sa.Boolean, default=False)
	city = sa.Column(sa.String, default="")
	email = sa.Column(sa.String, default="")
	fax = sa.Column(sa.String, default="")
	name = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=0)
	phone = sa.Column(sa.String, default="")
	zip = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('adresse1', "")
		kwargs.setdefault('adresse2', "")
		kwargs.setdefault('banner', "")
		kwargs.setdefault('cflag', False)
		kwargs.setdefault('city', "")
		kwargs.setdefault('email', "")
		kwargs.setdefault('fax', "")
		kwargs.setdefault('name', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('phone', "")
		kwargs.setdefault('zip', "")
		super(Cl_home, self).__init__(*args, **kwargs)
