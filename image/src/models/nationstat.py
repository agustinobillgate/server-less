from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Nationstat(Base):
	__tablename__ = 'nationstat'

	abrerwachs = sa.Column(sa.Integer, default=0)
	abrgratis = sa.Column(sa.Integer, default=0)
	abrkind1 = sa.Column(sa.Integer, default=0)
	abrkind2 = sa.Column(sa.Integer, default=0)
	ankerwachs = sa.Column(sa.Integer, default=0)
	ankgratis = sa.Column(sa.Integer, default=0)
	ankkind1 = sa.Column(sa.Integer, default=0)
	ankkind2 = sa.Column(sa.Integer, default=0)
	argtart = sa.Column(sa.Integer, default=2)
	betriebsnr = sa.Column(sa.Integer, default=0)
	dankerwachs = sa.Column(sa.Integer, default=0)
	dankgratis = sa.Column(sa.Integer, default=0)
	dankkind1 = sa.Column(sa.Integer, default=0)
	dankkind2 = sa.Column(sa.Integer, default=0)
	dankzimmer = sa.Column(sa.Integer, default=0)
	datum = sa.Column(sa.Date, default=None)
	dlogerwachs = sa.Column(sa.Integer, default=0)
	dloggratis = sa.Column(sa.Integer, default=0)
	dlogkind1 = sa.Column(sa.Integer, default=0)
	dlogkind2 = sa.Column(sa.Integer, default=0)
	logerwachs = sa.Column(sa.Integer, default=0)
	loggratis = sa.Column(sa.Integer, default=0)
	logkind1 = sa.Column(sa.Integer, default=0)
	logkind2 = sa.Column(sa.Integer, default=0)
	nationnr = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
