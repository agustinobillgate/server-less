#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Texte(Base):
	__tablename__ = 'texte'

	bez = sa.Column(sa.String, default="")
	language = sa.Column(sa.Integer, default=0)
	lupdate = sa.Column(sa.Date, default=get_current_date())
	notes = sa.Column(sa.String, default="")
	nr = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bez', "")
		kwargs.setdefault('language', 0)
		kwargs.setdefault('lupdate', get_current_date())
		kwargs.setdefault('notes', "")
		kwargs.setdefault('nr', 1)
		super(Texte, self).__init__(*args, **kwargs)
