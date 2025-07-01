#version: 1.0.0.2

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
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('kellner_nr', 0)
		kwargs.setdefault('normalbeleg', 1)
		kwargs.setdefault('roomcharge', False)
		kwargs.setdefault('tischnr', 0)
		super(Tisch, self).__init__(*args, **kwargs)
