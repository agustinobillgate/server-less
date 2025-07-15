#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Brieftmp(Base):
	__tablename__ = 'brieftmp'

	bediener_nr = sa.Column(sa.Integer, default=0)
	betrieb_gast = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	briefnr = sa.Column(sa.Integer, default=0)
	copies = sa.Column(sa.Integer, default=1)
	datum = sa.Column(sa.Date, default=get_current_date())
	drucken = sa.Column(sa.Boolean, default=False)
	flag = sa.Column(sa.Integer, default=0)
	gastnr = sa.Column(sa.Integer, default=0)
	kontakt_nr = sa.Column(sa.Integer, default=0)
	kortyp = sa.Column(sa.Integer, default=0)
	lfd__nr = sa.Column(sa.Integer, default=0)
	mahnbeginn = sa.Column(sa.Integer, default=0)
	mahnende = sa.Column(sa.Integer, default=0)
	millisek = sa.Column(sa.Integer, default=0)
	refdatum = sa.Column(sa.Date, default=get_current_date())
	resart = sa.Column(sa.Integer, default=1)
	resnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('bediener_nr', 0)
		kwargs.setdefault('betrieb_gast', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('briefnr', 0)
		kwargs.setdefault('copies', 1)
		kwargs.setdefault('datum', get_current_date())
		kwargs.setdefault('drucken', False)
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('gastnr', 0)
		kwargs.setdefault('kontakt_nr', 0)
		kwargs.setdefault('kortyp', 0)
		kwargs.setdefault('lfd__nr', 0)
		kwargs.setdefault('mahnbeginn', 0)
		kwargs.setdefault('mahnende', 0)
		kwargs.setdefault('millisek', 0)
		kwargs.setdefault('refdatum', get_current_date())
		kwargs.setdefault('resart', 1)
		kwargs.setdefault('resnr', 0)
		kwargs.setdefault('zeit', 0)
		super(Brieftmp, self).__init__(*args, **kwargs)
