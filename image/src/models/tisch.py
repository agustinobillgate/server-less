from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Tisch(Base):
	__tablename__ = 'tisch'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	kellner_nr = sa.Column(sa.Integer, default=0)
	normalbeleg = sa.Column(sa.Integer, default=1)
	roomcharge = sa.Column(sa.Boolean, default=False)
	tischnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
