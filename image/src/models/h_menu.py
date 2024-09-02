from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class H_menu(Base):
	__tablename__ = 'h_menu'

	artnr = sa.Column(sa.Integer, default=0)
	departement = sa.Column(sa.Integer, default=0)
	nr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
