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
