#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_untergrup(Base):
	__tablename__ = 'l_untergrup'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	fibukonto = sa.Column(sa.String, default="")
	zwkum = sa.Column(sa.Integer, default=0)
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('fibukonto', "")
		kwargs.setdefault('zwkum', 0)
		super(L_untergrup, self).__init__(*args, **kwargs)
