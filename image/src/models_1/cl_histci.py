#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Cl_histci(Base):
	__tablename__ = 'cl_histci'

	card_num = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	char2 = sa.Column(sa.String, default="")
	char3 = sa.Column(sa.String, default="")
	codenum = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=None)
	endtime = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	num1 = sa.Column(sa.Integer, default=0)
	num2 = sa.Column(sa.Integer, default=0)
	num3 = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	remarks = sa.Column(sa.String, default="")
	reslinnr = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	starttime = sa.Column(sa.Integer, default=0)
	voucherno = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('card_num', "")
		kwargs.setdefault('char1', "")
		kwargs.setdefault('char2', "")
		kwargs.setdefault('char3', "")
		kwargs.setdefault('codenum', "")
		kwargs.setdefault('datum', None)
		kwargs.setdefault('endtime', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('num1', 0)
		kwargs.setdefault('num2', 0)
		kwargs.setdefault('num3', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('remarks', "")
		kwargs.setdefault('reslinnr', 0)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('starttime', 0)
		kwargs.setdefault('voucherno', "")
		kwargs.setdefault('zinr', "")
		super(Cl_histci, self).__init__(*args, **kwargs)
