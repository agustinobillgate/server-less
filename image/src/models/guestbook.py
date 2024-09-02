from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Guestbook(Base):
	__tablename__ = 'guestbook'

	changed = sa.Column(sa.Date, default=None)
	cid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=lambda: get_current_date())
	gastnr = sa.Column(sa.Integer, default=0)
	imagefile = sa.Column(sa.LargeBinary, default=None)
	infostr = sa.Column(sa.String, default="")
	orig_infostr = sa.Column(sa.String, default="")
	reserve_char = sa.Column(ARRAY(sa.String),default=["","",""])
	reserve_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	reserve_logic = sa.Column(ARRAY(sa.Boolean),default=[False,False,False])
	userinit = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
