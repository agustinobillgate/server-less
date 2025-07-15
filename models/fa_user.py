#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Fa_user(Base):
	__tablename__ = 'fa_user'

	anzahl = sa.Column(sa.Integer, default=0)
	bis_datum = sa.Column(sa.Date, default=None)
	chgid = sa.Column(sa.String, default="")
	created = sa.Column(sa.Date, default=get_current_date())
	createdid = sa.Column(sa.String, default="")
	fa_status = sa.Column(sa.Integer, default=0)
	modifed = sa.Column(sa.Date, default=None)
	nr = sa.Column(sa.Integer, default=0)
	rcvid = sa.Column(sa.String, default="")
	rcvname = sa.Column(sa.String, default="")
	released = sa.Column(sa.Date, default=None)
	res_char = sa.Column(ARRAY(sa.String),default=["","",""])
	res_date = sa.Column(ARRAY(sa.Date),default=[None,None,None])
	res_int = sa.Column(ARRAY(sa.Integer),default=[0,0,0])
	res_logi = sa.Column(ARRAY(sa.Boolean),default=[False,False,False])
	vom_datum = sa.Column(sa.Date, default=None)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('anzahl', 0)
		kwargs.setdefault('bis_datum', None)
		kwargs.setdefault('chgid', "")
		kwargs.setdefault('created', get_current_date())
		kwargs.setdefault('createdid', "")
		kwargs.setdefault('fa_status', 0)
		kwargs.setdefault('modifed', None)
		kwargs.setdefault('nr', 0)
		kwargs.setdefault('rcvid', "")
		kwargs.setdefault('rcvname', "")
		kwargs.setdefault('released', None)
		kwargs.setdefault('res_char', ["","",""])
		kwargs.setdefault('res_date', [None,None,None])
		kwargs.setdefault('res_int', [0,0,0])
		kwargs.setdefault('res_logi', [False,False,False])
		kwargs.setdefault('vom_datum', None)
		super(Fa_user, self).__init__(*args, **kwargs)
