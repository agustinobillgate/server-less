#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Nitehist, Nitestor

def delete_nitehistbl(case_type:int, datum1:date, int1:int):

    prepare_cache ([Htparam, Nitestor])

    success_flag = False
    billdate:date = None
    htparam = nitehist = nitestor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, billdate, htparam, nitehist, nitestor
        nonlocal case_type, datum1, int1

        return {"success_flag": success_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    if case_type == 1:

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == datum1) & (Nitehist.reihenfolge == int1)).order_by(Nitehist._recid).with_for_update().all():
            db_session.delete(nitehist)
            pass
            success_flag = True

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.reihenfolge == int1)).order_by(Nitestor._recid).all():
            nitehist = Nitehist()
            db_session.add(nitehist)

            nitehist.datum = billdate
            nitehist.reihenfolge = nitestor.reihenfolge
            nitehist.line = nitestor.line
            nitehist.line_nr = nitestor.line_nr

    return generate_output()