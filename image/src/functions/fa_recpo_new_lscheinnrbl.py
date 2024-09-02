from functions.additional_functions import *
import decimal
from models import Fa_counter

def fa_recpo_new_lscheinnrbl(pr_973:bool, yy:int, mm:int):
    i = 0
    fa_counter = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, fa_counter


        return {"i": i}


    if pr_973:

        fa_counter = db_session.query(Fa_counter).filter(
                (Fa_counter.count_type == 0) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.dd == dd) &  (Fa_counter.docu_type == 1)).first()

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

        fa_counter = db_session.query(Fa_counter).filter(
                (Fa_counter.count_type == 1) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.docu_type == 1)).first()

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