#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mc_disc(Base):
	__tablename__ = 'mc_disc'

	artnrfront = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	discount = sa.Column(sa.Numeric, default=0)
	nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('artnrfront', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('discount', 0)
		kwargs.setdefault('nr', 0)
		super(Mc_disc, self).__init__(*args, **kwargs)
