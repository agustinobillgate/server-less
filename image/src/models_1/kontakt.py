#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kontakt(Base):
	__tablename__ = 'kontakt'

	abteilung = sa.Column(sa.String, default="")
	anrede = sa.Column(sa.String, default="")
	bankettnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	durchwahl = sa.Column(sa.String, default="")
	hauptkontakt = sa.Column(sa.Boolean, default=False)
	name = sa.Column(sa.String, default="")
	sprachcode = sa.Column(sa.Integer, default=1)
	vorname = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('abteilung', "")
		kwargs.setdefault('anrede', "")
		kwargs.setdefault('bankettnr', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('durchwahl', "")
		kwargs.setdefault('hauptkontakt', False)
		kwargs.setdefault('name', "")
		kwargs.setdefault('sprachcode', 1)
		kwargs.setdefault('vorname', "")
		super(Kontakt, self).__init__(*args, **kwargs)
