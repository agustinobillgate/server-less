#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_counter

def fa_recpo_new_lscheinnrbl(pr_973:bool, yy:int, mm:int):

    prepare_cache ([Fa_counter])

    i = 0
    fa_counter = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, fa_counter
        nonlocal pr_973, yy, mm

        return {"i": i}


    if pr_973:

        fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 0)],"yy": [(eq, yy)],"mm": [(eq, mm)],"dd": [(eq, dd)],"docu_type": [(eq, 1)]})

        if not fa_counter:
            fa_counter = Fa_counter()
            db_session.add(fa_counter)

            fa_counter.count_type = 0
            fa_counter.yy = yy
            fa_counter.mm = mm
            fa_counter.dd = dd
            fa_counter.counters = 0
            fa_counter.docu_type = 1


            i = fa_counter.counters + 1
        else:
            i = fa_counter.counters + 1
    else:

        fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 1)],"yy": [(eq, yy)],"mm": [(eq, mm)],"docu_type": [(eq, 1)]})

        if not fa_counter:
            fa_counter = Fa_counter()
            db_session.add(fa_counter)

            fa_counter.count_type = 1
            fa_counter.yy = yy
            fa_counter.mm = mm
            fa_counter.dd = 0
            fa_counter.counters = 0
            fa_counter.docu_type = 1


            i = fa_counter.counters + 1
        else:
            i = fa_counter.counters + 1

    return generate_output()