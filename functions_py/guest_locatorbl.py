#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def guest_locatorbl(resno:int, reslino:int, curr_s:string):

    prepare_cache ([Res_line])

    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line
        nonlocal resno, reslino, curr_s

        return {}


    # res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslino)]})
    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.reslinnr == reslino)).with_for_update().first()

    if res_line:
        res_line.voucher_nr = curr_s

    return generate_output()
