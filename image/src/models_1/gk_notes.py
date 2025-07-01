#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gk_notes(Base):
	__tablename__ = 'gk_notes'

	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	e_notes = sa.Column(sa.String, default="")
	gastnr = sa.Column(sa.Integer, default=None)
	notes = sa.Column(ARRAY(sa.String),default=["","","","","","","","","","","","","","","","","",""])
	page_nr = sa.Column(sa.Integer, default=0)
	program = sa.Column(sa.Integer, default=0)
	reslinnr = sa.Column(sa.Integer, default=0)
	resnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('e_notes', "")
		kwargs.setdefault('gastnr', None)
		kwargs.setdefault('notes', ["","","","","","","","","","","","","","","","","",""])
		kwargs.setdefault('page_nr', 0)
		kwargs.setdefault('program', 0)
		kwargs.setdefault('reslinnr', 0)
		kwargs.setdefault('resnr', 0)
		super(Gk_notes, self).__init__(*args, **kwargs)
