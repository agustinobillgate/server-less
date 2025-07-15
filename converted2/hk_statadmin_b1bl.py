#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def hk_statadmin_b1bl(bediener_nr_stat:int):

    prepare_cache ([Bediener])

    usrinit = ""
    avail_bediener = False
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal usrinit, avail_bediener, bediener
        nonlocal bediener_nr_stat

        return {"usrinit": usrinit, "avail_bediener": avail_bediener}


    bediener = get_cache (Bediener, {"nr": [(eq, bediener_nr_stat)]})

    if bediener:
        avail_bediener = True
        usrinit = bediener.userinit

    return generate_output()