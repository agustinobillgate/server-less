#version: 1.0.0.3

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class Gk_field(Base):
	__tablename__ = 'gk_field'

	betriebsnr = sa.Column(sa.Integer, default=0)
	compulsory = sa.Column(sa.Boolean, default=False)
	default_width = sa.Column(sa.Numeric, default=0)
	feldtyp = sa.Column(sa.String, default="fill-in")
	field_column = sa.Column(sa.Numeric, default=0)
	field_height = sa.Column(sa.Numeric, default=1)
	field_name = sa.Column(sa.String, default=None)
	field_order = sa.Column(sa.Integer, default=0)
	field_row = sa.Column(sa.Numeric, default=0)
	field_width = sa.Column(sa.Numeric, default=0)
	flag = sa.Column(sa.Integer, default=0)
	karteityp = sa.Column(sa.Integer, default=0)
	label_pos = sa.Column(sa.Integer, default=0)
	private_data = sa.Column(sa.String, default="")
	updateable = sa.Column(sa.Boolean, default=False)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('compulsory', False)
		kwargs.setdefault('default_width', 0)
		kwargs.setdefault('feldtyp', "fill-in")
		kwargs.setdefault('field_column', 0)
		kwargs.setdefault('field_height', 1)
		kwargs.setdefault('field_name', None)
		kwargs.setdefault('field_order', 0)
		kwargs.setdefault('field_row', 0)
		kwargs.setdefault('field_width', 0)
		kwargs.setdefault('flag', 0)
		kwargs.setdefault('karteityp', 0)
		kwargs.setdefault('label_pos', 0)
		kwargs.setdefault('private_data', "")
		kwargs.setdefault('updateable', False)
		super(Gk_field, self).__init__(*args, **kwargs)
