#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Notes(Base):
	__tablename__ = 'notes'

	bediener_nr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	dept = sa.Column(sa.String, default="")
	note = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","","",""])
	page_nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('dept', "")
		kwargs.setdefault('note', ["","","","","","","","","","","","","","","","","","",""])
		kwargs.setdefault('page_nr', 0)
		super(Notes, self).__init__(*args, **kwargs)
