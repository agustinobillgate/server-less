#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Sourccod

def restype_admin_btn_delbl(source_code:int):
    flag = False
    success_flag = False
    reservation = sourccod = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, success_flag, reservation, sourccod
        nonlocal source_code

        return {"flag": flag, "success_flag": success_flag}


    reservation = get_cache (Reservation, {"resart": [(eq, source_code)]})

    if reservation:
        flag = True
    else:

        # sourccod = get_cache (Sourccod, {"source_code": [(eq, source_code)]})
        sourccod = db_session.query(Sourccod).filter(
                 (Sourccod.source_code == source_code)).with_for_update().first()
        db_session.delete(sourccod)
        success_flag = True

    return generate_output()