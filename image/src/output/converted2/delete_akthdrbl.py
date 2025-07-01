#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr

def delete_akthdrbl(case_type:int, aktnr:int):
    success_flag = False
    akthdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akthdr
        nonlocal case_type, aktnr

        return {"success_flag": success_flag}


    if case_type == 1:

        akthdr = get_cache (Akthdr, {"aktnr": [(eq, aktnr)]})

        if akthdr:
            db_session.delete(akthdr)
            pass
            success_flag = True

    return generate_output()