#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Iftable(Base):
	__tablename__ = 'iftable'

	betriebsnr = sa.Column(sa.Integer, default=0)
	credit_nr = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0])
	departement = sa.Column(sa.String, default="")
	mwst = sa.Column(ARRAY(sa.Integer),default=[0,0,0,0,0])
	waiter_id = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('credit_nr', [0,0,0,0,0])
		kwargs.setdefault('departement', "")
		kwargs.setdefault('mwst', [0,0,0,0,0])
		kwargs.setdefault('waiter_id', 0)
		super(Iftable, self).__init__(*args, **kwargs)
