from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Hrbeleg(Base):
	__tablename__ = 'hrbeleg'

	betriebsnr = sa.Column(sa.Integer, default=0)
	couverts_eff = sa.Column(sa.Integer, default=0)
	couverts100 = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=lambda: get_current_date())
	departement = sa.Column(sa.Integer, default=0)
	gesamtumsatz = sa.Column(sa.Numeric, default=0)
	hour = sa.Column(sa.Integer, default=0)
	intervall = sa.Column(sa.Integer, default=0)
	tischbel_eff = sa.Column(sa.Integer, default=0)
	tischbel100 = sa.Column(sa.Integer, default=0)
	umsatzanw = sa.Column(sa.Numeric, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
