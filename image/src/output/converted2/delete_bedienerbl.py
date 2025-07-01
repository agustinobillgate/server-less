#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def delete_bedienerbl(case_type:int, int1:int, int2:int, char1:string):
    success_flag = False
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bediener
        nonlocal case_type, int1, int2, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        bediener = get_cache (Bediener, {"nr": [(eq, int1)]})

        if bediener:
            db_session.delete(bediener)
            pass
            success_flag = True

    return generate_output()