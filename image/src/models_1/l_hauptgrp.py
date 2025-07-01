#version: 1.0.0.2

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa
from models.base import Base
from functions.additional_functions import get_current_date

class L_hauptgrp(Base):
	__tablename__ = 'l_hauptgrp'

	betriebsnr = sa.Column(sa.Integer, default=0)
	bezeich = sa.Column(sa.String, default="")
	endkum = sa.Column(sa.Integer, default=0)
	fibukonto = sa.Column(sa.String, default="")
	_recid = sa.Column(sa.Integer, primary_key=True)
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('betriebsnr', 0)
		kwargs.setdefault('bezeich', "")
		kwargs.setdefault('endkum', 0)
		kwargs.setdefault('fibukonto', "")
		super(L_hauptgrp, self).__init__(*args, **kwargs)
