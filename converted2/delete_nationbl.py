#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def delete_nationbl(case_type:int, int1:int, char1:string):
    success_flag = False
    nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nation
        nonlocal case_type, int1, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        nation = get_cache (Nation, {"nationnr": [(eq, int1)],"kurzbez": [(eq, char1)]})

        if nation:
            db_session.delete(nation)
            pass
            success_flag = True
    elif case_type == 2:

        nation = get_cache (Nation, {"_recid": [(eq, int1)]})

        if nation:
            db_session.delete(nation)
            pass
            success_flag = True

    return generate_output()