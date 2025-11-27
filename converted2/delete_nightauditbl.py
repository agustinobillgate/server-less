#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Nightaudit

def delete_nightauditbl(case_type:int, int1:int):
    successflag = False
    nightaudit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, nightaudit
        nonlocal case_type, int1

        return {"successflag": successflag}


    if case_type == 1:

        # nightaudit = get_cache (Nightaudit, {"_recid": [(eq, int1)]})
        nightaudit = db_session.query(Nightaudit).filter(
                 (Nightaudit._recid == int1)).with_for_update().first()

        if nightaudit:
            db_session.delete(nightaudit)
            pass
            successflag = True

    return generate_output()