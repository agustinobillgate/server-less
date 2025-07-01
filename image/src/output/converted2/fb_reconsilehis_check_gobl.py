#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_besthis

def fb_reconsilehis_check_gobl(from_date:date):
    avail_l_besthis = False
    l_besthis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_besthis, l_besthis
        nonlocal from_date

        return {"avail_l_besthis": avail_l_besthis}


    l_besthis = get_cache (L_besthis, {"anf_best_dat": [(eq, from_date)]})

    if l_besthis:
        avail_l_besthis = True

    return generate_output()