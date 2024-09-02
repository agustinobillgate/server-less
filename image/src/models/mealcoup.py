from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Mealcoup(Base):
	__tablename__ = 'mealcoup'

	abreise = sa.Column(sa.Date, default=lambda: get_current_date())
	activeflag = sa.Column(sa.Boolean, default=True)
	ankunft = sa.Column(sa.Date, default=lambda: get_current_date())
	anzahl = sa.Column(sa.Integer, default=0)
	name = sa.Column(sa.String, default="")
	resnr = sa.Column(sa.Integer, default=0)
	verbrauch = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
