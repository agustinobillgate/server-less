from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class B_oorder(Base):
	__tablename__ = 'b_oorder'

	artnr = sa.Column(sa.Integer, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bis_zeit = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	gespende = sa.Column(sa.Date, default=None)
	gespgrund = sa.Column(sa.String, default="")
	gespstart = sa.Column(sa.Date, default=None)
	raum = sa.Column(sa.String, default="")
	von_zeit = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
