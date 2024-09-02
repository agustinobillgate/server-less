from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class K_history(Base):
	__tablename__ = 'k_history'

	comment = sa.Column(sa.String, default="")
	diet_adv = sa.Column(sa.String, default="")
	doctor_adv = sa.Column(sa.String, default="")
	from_date = sa.Column(sa.Date, default=None)
	gastnr = sa.Column(sa.Integer, default=0)
	gwish = sa.Column(sa.String, default="")
	id = sa.Column(sa.String, default="")
	info1 = sa.Column(sa.String, default="")
	info2 = sa.Column(sa.String, default="")
	resnr = sa.Column(sa.Integer, default=0)
	to_date = sa.Column(sa.Date, default=None)
	treatment = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
