#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akt_line, Akt_code

def aktcode_admin_btn_delnamebl(akt_code_aktionscode:int, recid_akt_code:int):
    erase_flag = False
    akt_line = akt_code = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal erase_flag, akt_line, akt_code
        nonlocal akt_code_aktionscode, recid_akt_code

        return {"erase_flag": erase_flag}


    akt_line = get_cache (Akt_line, {"aktionscode": [(eq, akt_code_aktionscode)]})

    if akt_line:
        pass
    else:

        # akt_code = get_cache (Akt_code, {"_recid": [(eq, recid_akt_code)]})
        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code._recid == recid_akt_code)).with_for_update().first()

        if akt_code:
            pass
            db_session.delete(akt_code)
            erase_flag = True

    return generate_output()