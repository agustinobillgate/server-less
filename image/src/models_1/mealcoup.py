#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mealcoup(Base):
	__tablename__ = 'mealcoup'

	abreise = sa.Column(sa.Date, default=get_current_date())
	activeflag = sa.Column(sa.Boolean, default=True)
	ankunft = sa.Column(sa.Date, default=get_current_date())
	anzahl = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	resnr = sa.Column(sa.Integer, default=0)
	verbrauch = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('abreise', get_current_date())
		kwargs.setdefault('activeflag', True)
		kwargs.setdefault('ankunft', get_current_date())
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('name', "")
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('verbrauch', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		kwargs.setdefault('zinr', "")
		super(Mealcoup, self).__init__(*args, **kwargs)
