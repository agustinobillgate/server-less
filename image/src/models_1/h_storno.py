#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_storno(Base):
	__tablename__ = 'h_storno'

	aendertext = sa.Column(sa.String, default="")
	anzahl = sa.Column(sa.Integer, default=0)
	artart = sa.Column(sa.Integer, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	artnrfront = sa.Column(sa.Integer, default=0)
	betrag = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	bill_datum = sa.Column(sa.Date, default=None)
	buchflag = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	epreis = sa.Column(sa.Numeric, default=0)
	kellner_nr = sa.Column(sa.Integer, default=0)
	rechnr = sa.Column(sa.Integer, default=0)
	steuercode = sa.Column(sa.Integer, default=0)
	stornogrund = sa.Column(sa.String, default="")
	sysdate = sa.Column(sa.Date, default=get_current_date())
	tischnr = sa.Column(sa.Integer, default=0)
	trinkgeld = sa.Column(sa.Numeric, default=0)
	waehrungcode = sa.Column(sa.Integer, default=0)
	waehrungsnr = sa.Column(sa.Integer, default=0)
	zeit = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('aendertext', "")
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('artart', 0)
		kwargs.setdefault('artnr', 0)
		kwargs.setdefault('artnrfront', 0)
		kwargs.setdefault('betrag', 0)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('bill_datum', None)
		kwargs.setdefault('buchflag', 0)
		kwargs.setdefault('departement', 0)
		kwargs.setdefault('epreis', 0)
		kwargs.setdefault('kellner_nr', 0)
		kwargs.setdefault('rechnr', 0)
		kwargs.setdefault('steuercode', 0)
		kwargs.setdefault('stornogrund', "")
		kwargs.setdefault('sysdate', get_current_date())
		kwargs.setdefault('tischnr', 0)
		kwargs.setdefault('trinkgeld', 0)
		kwargs.setdefault('waehrungcode', 0)
		kwargs.setdefault('waehrungsnr', 0)
		kwargs.setdefault('zeit', 0)
		kwargs.setdefault('zinr', "")
		super(H_storno, self).__init__(*args, **kwargs)
