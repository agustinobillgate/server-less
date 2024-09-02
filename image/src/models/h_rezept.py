from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_rezept(Base):
	__tablename__ = 'h_rezept'

	artnrrezept = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	datumanlage = sa.Column(sa.Date, default=None)
	datummod = sa.Column(sa.Date, default=None)
	kategorie = sa.Column(sa.Integer, default=0)
	portion = sa.Column(sa.Integer, default=1)
	_recid = sa.Column(sa.Integer, primary_key=True)
