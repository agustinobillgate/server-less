#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def delete_hoteldptbl(case_type:int, int1:int, int2:int, char1:string):
    success_flag = False
    hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, hoteldpt
        nonlocal case_type, int1, int2, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, int1)]})
        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == int1)).with_for_update().first()

        if hoteldpt:
            db_session.delete(hoteldpt)
            pass
            success_flag = True

    return generate_output()