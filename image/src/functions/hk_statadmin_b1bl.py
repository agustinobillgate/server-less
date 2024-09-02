from functions.additional_functions import *
import decimal
from models import Bediener

def hk_statadmin_b1bl(bediener_nr_stat:int):
    usrinit = ""
    avail_bediener = False
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal usrinit, avail_bediener, bediener


        return {"usrinit": usrinit, "avail_bediener": avail_bediener}


    bediener = db_session.query(Bediener).filter(
            (Bediener.nr == bediener_nr_stat)).first()

    if bediener:
        avail_bediener = True
        usrinit = bediener.userinit

    return generate_output()