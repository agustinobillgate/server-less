#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mathis(Base):
	__tablename__ = 'mathis'

	asset = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=get_current_date())
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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('asset', "")
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('fname', "")
		kwargs.setdefault('location', "")
		kwargs.setdefault('mark', "")
		kwargs.setdefault('model', "")
		kwargs.setdefault('name', "")
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('price', 0)
		kwargs.setdefault('remark', "")
		kwargs.setdefault('spec', "")
		kwargs.setdefault('supplier', "")
		super(Mathis, self).__init__(*args, **kwargs)
