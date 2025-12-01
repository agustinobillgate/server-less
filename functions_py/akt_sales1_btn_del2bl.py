#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akt_line

def akt_sales1_btn_del2bl(recid_aktline:int):
    akt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_line
        nonlocal recid_aktline

        return {}


    # akt_line = get_cache (Akt_line, {"_recid": [(eq, recid_aktline)]})
    akt_line = db_session.query(Akt_line).filter(Akt_line._recid == recid_aktline).with_for_update().first()
    db_session.delete(akt_line)

    return generate_output()