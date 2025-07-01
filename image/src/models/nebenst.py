#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nebenst(Base):
	__tablename__ = 'nebenst'

	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	nebenstelle = sa.Column(sa.String, default="")
	nebst_type = sa.Column(sa.Integer, default=0)
	nebstart = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	vipnr = sa.Column(sa.String, default="")
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('nebenstelle', "")
		kwargs.setdefault('nebst_type', 0)
		kwargs.setdefault('nebstart', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('vipnr', "")
		kwargs.setdefault('zinr', "")
		super(Nebenst, self).__init__(*args, **kwargs)
