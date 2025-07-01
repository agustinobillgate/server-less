#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mhis_line(Base):
	__tablename__ = 'mhis_line'

	cost = sa.Column(sa.Numeric, default=0)
	datum = sa.Column(sa.Date, default=get_current_date())
	nr = sa.Column(sa.Integer, default=0)
	remark = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('cost', 0)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('remark', "")
		super(Mhis_line, self).__init__(*args, **kwargs)
