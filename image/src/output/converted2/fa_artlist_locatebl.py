#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager

def fa_artlist_locatebl(locate:string):
    avail_fa_lager = False
    fa_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_fa_lager, fa_lager
        nonlocal locate

        return {"avail_fa_lager": avail_fa_lager}


    fa_lager = get_cache (Fa_lager, {"bezeich": [(eq, locate)]})

    if fa_lager:
        avail_fa_lager = True

    return generate_output()