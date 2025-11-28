#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_counter

def fa_recpo_update_lscheinnrbl(pr_973:bool, yy:int, mm:int, dd:int):

    prepare_cache ([Fa_counter])

    fa_counter = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_counter
        nonlocal pr_973, yy, mm, dd

        return {}


    if pr_973:

        # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 0)],"yy": [(eq, yy)],"mm": [(eq, mm)],"dd": [(eq, dd)],"docu_type": [(eq, 1)]})
        fa_counter = db_session.query(Fa_counter).filter(
                 (Fa_counter.count_type == 0) &
                 (Fa_counter.yy == yy) &
                 (Fa_counter.mm == mm) &
                 (Fa_counter.dd == dd) &
                 (Fa_counter.docu_type == 1)).with_for_update().first()

        if not fa_counter:
            fa_counter = Fa_counter()
            db_session.add(fa_counter)

            fa_counter.count_type = 0
            fa_counter.yy = yy
            fa_counter.mm = mm
            fa_counter.dd = dd
            fa_counter.counters = 0
            fa_counter.docu_type = 1


        else:
            pass
            fa_counter.counters = fa_counter.counters + 1
            db_session.refresh(fa_counter,with_for_update=True)
            pass
    else:

        # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 1)],"yy": [(eq, yy)],"mm": [(eq, mm)],"docu_type": [(eq, 1)]})
        fa_counter = db_session.query(Fa_counter).filter(
                 (Fa_counter.count_type == 1) &
                 (Fa_counter.yy == yy) &
                 (Fa_counter.mm == mm) &
                 (Fa_counter.docu_type == 1)).with_for_update().first()

        if not fa_counter:
            fa_counter = Fa_counter()
            db_session.add(fa_counter)

            fa_counter.count_type = 1
            fa_counter.yy = yy
            fa_counter.mm = mm
            fa_counter.dd = 0
            fa_counter.counters = 0
            fa_counter.docu_type = 1


        else:
            pass
            fa_counter.counters = fa_counter.counters + 1
            db_session.refresh(fa_counter,with_for_update=True)
            pass

    return generate_output()
