#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_resumz_listbl():

    prepare_cache ([Htparam])

    long_digit = False
    to_date = None
    ldry = 0
    dstore = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    t_hoteldpt_list = []
    min_dept:int = 0
    max_dept:int = 0
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, to_date, ldry, dstore, from_dept, to_dept, depname1, depname2, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"long_digit": long_digit, "to_date": to_date, "ldry": ldry, "dstore": dstore, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal long_digit, to_date, ldry, dstore, from_dept, to_dept, depname1, depname2, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger
        min_dept = 0

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num
        from_dept = min_dept
        to_dept = max_dept

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})

        if hoteldpt:
            depname1 = hoteldpt.depart

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})

        if hoteldpt:
            depname2 = hoteldpt.depart


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    to_date = get_current_date()
    select_dept()

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()