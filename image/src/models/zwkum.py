from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zwkum(Base):
	__tablename__ = 'zwkum'

	bankett = sa.Column(sa.Boolean, default=False)
	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	departement = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="")
	hotelrest = sa.Column(sa.Boolean, default=False)
	mwstsplit = sa.Column(sa.Boolean, default=False)
	steuercod1 = sa.Column(sa.Integer, default=0)
	steuercod2 = sa.Column(sa.Integer, default=0)
	zknr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
