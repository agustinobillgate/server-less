#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def mk_resline_rnextbl(resnr:int, reslinnr:int, t_zipreis:Decimal):

    prepare_cache ([Res_line])

    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line
        nonlocal resnr, reslinnr, t_zipreis

        return {}


    # res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).with_for_update().first()

    if res_line:
        res_line.zipreis =  to_decimal(t_zipreis)

    return generate_output()
