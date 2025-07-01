#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Sourcetext(Base):
	__tablename__ = 'sourcetext'

	flag1 = sa.Column(sa.Integer, default=0)
	refcode = sa.Column(sa.Integer, default=0)
	refcontext = sa.Column(sa.String, default="")
	reftext = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('flag1', 0)
		kwargs.setdefault('refcode', 0)
		kwargs.setdefault('refcontext', "")
		kwargs.setdefault('reftext', "")
		super(Sourcetext, self).__init__(*args, **kwargs)
