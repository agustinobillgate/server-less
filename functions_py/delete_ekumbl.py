#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Ekum

def delete_ekumbl(case_type:int, int1:int, char1:string):
    success_flag = False
    ekum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, ekum
        nonlocal case_type, int1, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        # ekum = get_cache (Ekum, {"eknr": [(eq, int1)],"bezeich": [(eq, char1)]})
        ekum = db_session.query(Ekum).filter(
                 (Ekum.eknr == int1) &
                 (Ekum.bezeich == char1)).with_for_update().first()

        if ekum:
            db_session.delete(ekum)
            pass
            success_flag = True

    return generate_output()