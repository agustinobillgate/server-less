#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def competitor_adm_leave_slist_hnrbl(slist_hnr:int):

    prepare_cache ([Akt_code])

    avail_akt_code = False
    akt_code_bezeich = ""
    akt_code = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_akt_code, akt_code_bezeich, akt_code
        nonlocal slist_hnr

        return {"avail_akt_code": avail_akt_code, "akt_code_bezeich": akt_code_bezeich}


    akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, slist_hnr)]})

    if akt_code:
        avail_akt_code = True
        akt_code_bezeich = akt_code.bezeich

    return generate_output()