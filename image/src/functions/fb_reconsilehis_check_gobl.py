from functions.additional_functions import *
import decimal
from datetime import date
from models import L_besthis

def fb_reconsilehis_check_gobl(from_date:date):
    avail_l_besthis = False
    l_besthis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_besthis, l_besthis


        return {"avail_l_besthis": avail_l_besthis}


    l_besthis = db_session.query(L_besthis).filter(
            (L_besthis.anf_best_dat == from_date)).first()

    if l_besthis:
        avail_l_besthis = True

    return generate_output()