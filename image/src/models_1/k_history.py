#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class K_history(Base):
	__tablename__ = 'k_history'

	comment = sa.Column(sa.String, default="")
	diet_adv = sa.Column(sa.String, default="")
	doctor_adv = sa.Column(sa.String, default="")
	from_date = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=0)
	gwish = sa.Column(sa.String, default="")
	id = sa.Column(sa.String, default="")
	info1 = sa.Column(sa.String, default="")
	info2 = sa.Column(sa.String, default="")
	resnr = sa.Column(sa.Integer, default=0)
	to_date = sa.Column(sa.Date, default=None)
	treatment = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('comment', "")
		kwargs.setdefault('diet_adv', "")
		kwargs.setdefault('doctor_adv', "")
		kwargs.setdefault('from_date', None)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('gwish', "")
		kwargs.setdefault('id', "")
		kwargs.setdefault('info1', "")
		kwargs.setdefault('info2', "")
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('to_date', None)
		kwargs.setdefault('treatment', "")
		super(K_history, self).__init__(*args, **kwargs)
