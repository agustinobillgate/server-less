#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep

t_wgrpdep_list, T_wgrpdep = create_model_like(Wgrpdep)

def write_wgrpdepbl(case_type:int, t_wgrpdep_list:[T_wgrpdep]):
    success_flag = False
    curr_counter:int = 1
    wgrpdep = None

    t_wgrpdep = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_counter, wgrpdep
        nonlocal case_type


        nonlocal t_wgrpdep

        return {"success_flag": success_flag}

    t_wgrpdep = query(t_wgrpdep_list, first=True)

    if not t_wgrpdep:

        return generate_output()

    if case_type == 1:

        if t_wgrpdep.zknr == 0:

            for wgrpdep in db_session.query(Wgrpdep).filter(
                     (Wgrpdep.departement == t_wgrpdep.departement)).order_by(Wgrpdep.zknr.desc()).yield_per(100):
                curr_counter = wgrpdep.zknr + 1
                break
            t_wgrpdep.zknr = curr_counter


        wgrpdep = Wgrpdep()
        db_session.add(wgrpdep)

        buffer_copy(t_wgrpdep, wgrpdep)
        pass
        success_flag = True
    elif case_type == 2:

        wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, t_wgrpdep.zknr)],"departement": [(eq, t_wgrpdep.departement)]})

        if wgrpdep:
            buffer_copy(t_wgrpdep, wgrpdep)
            pass
            pass
            success_flag = True
    elif case_type == 3:

        wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, t_wgrpdep.zknr)],"departement": [(eq, t_wgrpdep.departement)]})

        if wgrpdep:
            db_session.delete(wgrpdep)
            pass
            success_flag = True

    return generate_output()