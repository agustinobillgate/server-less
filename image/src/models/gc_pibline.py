#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gc_pibline(Base):
	__tablename__ = 'gc_pibline'

	created = sa.Column(sa.Date, default=None)
	docu_nr = sa.Column(sa.String, default="")
	inv_acctno = sa.Column(sa.String, default="")
	inv_amount = sa.Column(sa.Numeric, default=0)
	inv_bemerk = sa.Column(sa.String, default="")
	inv_bezeich = sa.Column(sa.String, default="")
	invoice_nr = sa.Column(sa.String, default="")
	lief_nr = sa.Column(sa.Integer, default=0)
	supplier = sa.Column(sa.String, default="")
	zeit = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('created', None)
		kwargs.setdefault('docu_nr', "")
		kwargs.setdefault('inv_acctno', "")
		kwargs.setdefault('inv_amount', 0)
		kwargs.setdefault('inv_bemerk', "")
		kwargs.setdefault('inv_bezeich', "")
		kwargs.setdefault('invoice_nr', "")
		kwargs.setdefault('lief_nr', 0)
		kwargs.setdefault('supplier', "")
		kwargs.setdefault('zeit', 0)
		super(Gc_pibline, self).__init__(*args, **kwargs)
