#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Outorder

def read_outorderbl(case_type:int, rmno:string, resno:int, ci_date:date, to_date:date):
    t_outorder_data = []
    outorder = None

    t_outorder = None

    t_outorder_data, T_outorder = create_model_like(Outorder)

    db_session = local_storage.db_session
    rmno = rmno.strip()

    def generate_output():
        nonlocal t_outorder_data, outorder
        nonlocal case_type, rmno, resno, ci_date, to_date


        nonlocal t_outorder
        nonlocal t_outorder_data

        return {"t-outorder": t_outorder_data}

    if case_type == 1:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"betriebsnr": [(eq, resno)]})
    elif case_type == 2:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)]})
    elif case_type == 3:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"gespstart": [(ge, ci_date)],"gespende": [(le, ci_date)]})
    elif case_type == 4:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"gespende": [(ge, ci_date)]})
    elif case_type == 5:

        outorder = get_cache (Outorder, {"_recid": [(eq, resno)]})
    elif case_type == 6:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)],"betriebsnr": [(le, 1)]})
    elif case_type == 7:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"betriebsnr": [(eq, resno)],"gespstart": [(gt, to_date)],"gespende": [(lt, ci_date)]})
    elif case_type == 99:

        outorder = get_cache (Outorder, {"zinr": [(eq, rmno)],"betriebsnr": [(eq, resno)]})

    if outorder:
        t_outorder = T_outorder()
        t_outorder_data.append(t_outorder)

        buffer_copy(outorder, t_outorder)

    return generate_output()