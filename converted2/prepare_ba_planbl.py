#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Htparam, Bk_reser

def prepare_ba_planbl():

    prepare_cache ([Htparam])

    ci_date = None
    ba_dept = 0
    run_beowarning = False
    p_900 = 0
    t_bk_raum_data = []
    bk_raum = htparam = bk_reser = None

    t_bk_raum = None

    t_bk_raum_data, T_bk_raum = create_model_like(Bk_raum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, ba_dept, run_beowarning, p_900, t_bk_raum_data, bk_raum, htparam, bk_reser


        nonlocal t_bk_raum
        nonlocal t_bk_raum_data

        return {"ci_date": ci_date, "ba_dept": ba_dept, "run_beowarning": run_beowarning, "p_900": p_900, "t-bk-raum": t_bk_raum_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
    ba_dept = htparam.finteger

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_data.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)

    bk_reser = get_cache (Bk_reser, {"datum": [(eq, ci_date)],"fakturiert": [(eq, 1)]})

    if bk_reser:
        run_beowarning = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    if htparam:
        p_900 = htparam.finteger

    return generate_output()