#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mc_cardhis(Base):
	__tablename__ = 'mc_cardhis'

	char1 = sa.Column(sa.String, default="")
	datum = sa.Column(sa.Date, default=get_current_date())
	gastnr = sa.Column(sa.Integer, default=0)
	new_card = sa.Column(sa.String, default="")
	new_nr = sa.Column(sa.Integer, default=0)
	old_card = sa.Column(sa.String, default="")
	old_nr = sa.Column(sa.Integer, default=0)
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('char1', "")
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('new_card', "")
		kwargs.setdefault('new_nr', 0)
		kwargs.setdefault('old_card', "")
		kwargs.setdefault('old_nr', 0)
		kwargs.setdefault('userinit', "")
		kwargs.setdefault('zeit', 0)
		super(Mc_cardhis, self).__init__(*args, **kwargs)
