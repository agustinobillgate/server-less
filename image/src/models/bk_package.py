from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Bk_package(Base):
	__tablename__ = 'bk_package'

	anzahl = sa.Column(sa.Integer, default=0)
	arrangemdat = sa.Column(sa.Date, default=None)
	arrangement = sa.Column(sa.String, default="")
	artnr = sa.Column(sa.Integer, default=0)
	bemerkung = sa.Column(sa.String, default="")
	betrag = sa.Column(sa.Numeric, default=0)
	betrieb_gastver = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	bis_datum = sa.Column(sa.Date, default=None)
	bis_i = sa.Column(sa.Integer, default=0)
	bis_zeit = sa.Column(sa.String, default="")
	char1 = sa.Column(sa.String, default="")
	date1 = sa.Column(sa.Date, default=None)
	datum = sa.Column(sa.Date, default=None)
	deci1 = sa.Column(sa.Numeric, default=0)
	departement = sa.Column(sa.Integer, default=0)
	fakturiert = sa.Column(sa.Integer, default=0)
	gastnrver = sa.Column(sa.Integer, default=0)
	logi1 = sa.Column(sa.Boolean, default=False)
	notizen = sa.Column(sa.String, default="")
	number1 = sa.Column(sa.Integer, default=0)
	personen = sa.Column(sa.Integer, default=0)
	preis = sa.Column(sa.Numeric, default=0)
	raum = sa.Column(sa.String, default="")
	raum_bez = sa.Column(sa.String, default="")
	veran_nr = sa.Column(sa.Integer, default=0)
	veran_resnr = sa.Column(sa.Integer, default=0)
	von_i = sa.Column(sa.Integer, default=0)
	von_zeit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
