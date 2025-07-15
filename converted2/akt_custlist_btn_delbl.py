#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_cust, Akthdr

def akt_custlist_btn_delbl(a_gastnr:int, rec_id:int):
    err = 0
    akt_cust = akthdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_cust, akthdr
        nonlocal a_gastnr, rec_id

        return {"err": err}


    akt_cust = get_cache (Akt_cust, {"_recid": [(eq, rec_id)]})

    akthdr = get_cache (Akthdr, {"gastnr": [(eq, a_gastnr)]})

    if akthdr:
        err = 1
    pass
    db_session.delete(akt_cust)

    return generate_output()