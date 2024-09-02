from functions.additional_functions import *
import decimal
from models import Fa_counter

def fa_recpo_update_lscheinnrbl(pr_973:bool, yy:int, mm:int):
    fa_counter = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_counter


        return {}


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


        else:

            fa_counter = db_session.query(Fa_counter).first()
            fa_counter.counters = fa_counter.counters + 1

            fa_counter = db_session.query(Fa_counter).first()
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


        else:

            fa_counter = db_session.query(Fa_counter).first()
            fa_counter.counters = fa_counter.counters + 1

            fa_counter = db_session.query(Fa_counter).first()

    return generate_output()