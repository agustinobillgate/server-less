#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def arl_list_add_keycard1bl(recid_rline:int):

    prepare_cache ([Res_line])

    res_line = None

    rline = None

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line
        nonlocal recid_rline
        nonlocal rline


        nonlocal rline

        return {}


    # rline = get_cache (Res_line, {"_recid": [(eq, recid_rline)]})
    rline = db_session.query(Res_line).filter(Res_line._recid == recid_rline).with_for_update().first()

    if rline:
        pass
        rline.betrieb_gast = rline.betrieb_gast + 1
        # pass
        # pass
        db_session.refresh(rline, with_for_update=True)

    return generate_output()