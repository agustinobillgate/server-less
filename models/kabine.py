#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Kabine(Base):
	__tablename__ = 'kabine'

	anzpers = sa.Column(sa.Integer, default=1)
	betriebsnr = sa.Column(sa.Integer, default=0)
	fdate = sa.Column(sa.Date, default=None)
	gesperrt = sa.Column(sa.Boolean, default=False)
	grund = sa.Column(sa.String, default="")
	kabbez = sa.Column(sa.String, default="")
	kabnr = sa.Column(sa.Integer, default=0)
	massnr = sa.Column(sa.Integer, default=0)
	offenab = sa.Column(sa.String, default="00:00")
	offenbis = sa.Column(sa.String, default="00:00")
	oooab = sa.Column(sa.String, default="00:00")
	ooobis = sa.Column(sa.String, default="00:00")
	pauseab = sa.Column(sa.String, default="00:00")
	pausebis = sa.Column(sa.String, default="00:00")
	tdate = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzpers', 1)
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('fdate', None)
		kwargs.setdefault('gesperrt', False)
		kwargs.setdefault('grund', "")
		kwargs.setdefault('kabbez', "")
		kwargs.setdefault('kabnr', 0)
		kwargs.setdefault('massnr', 0)
		kwargs.setdefault('offenab', "00:00")
		kwargs.setdefault('offenbis', "00:00")
		kwargs.setdefault('oooab', "00:00")
		kwargs.setdefault('ooobis', "00:00")
		kwargs.setdefault('pauseab', "00:00")
		kwargs.setdefault('pausebis', "00:00")
		kwargs.setdefault('tdate', None)
		super(Kabine, self).__init__(*args, **kwargs)
