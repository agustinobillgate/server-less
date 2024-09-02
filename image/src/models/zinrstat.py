from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Zinrstat(Base):
	__tablename__ = 'zinrstat'

	argtumsatz = sa.Column(sa.Numeric, default=0)
	betriebsnr = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	logisumsatz = sa.Column(sa.Numeric, default=0)
	personen = sa.Column(sa.Integer, default=0)
	zimmeranz = sa.Column(sa.Integer, default=0)
	zinr = sa.Column(sa.String, default="1")
	_recid = sa.Column(sa.Integer, primary_key=True)
