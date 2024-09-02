from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Wgrpgen(Base):
	__tablename__ = 'wgrpgen'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	eknr = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
