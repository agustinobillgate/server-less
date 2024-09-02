from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_besthis(Base):
	__tablename__ = 'l_besthis'

	anf_best_dat = sa.Column(sa.Date, default=lambda: get_current_date())
	anz_anf_best = sa.Column(sa.Numeric, default=0)
	anz_ausgang = sa.Column(sa.Numeric, default=0)
	anz_eingang = sa.Column(sa.Numeric, default=0)
	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	lager_nr = sa.Column(sa.Integer, default=0)
	val_anf_best = sa.Column(sa.Numeric, default=0)
	wert_ausgang = sa.Column(sa.Numeric, default=0)
	wert_eingang = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
