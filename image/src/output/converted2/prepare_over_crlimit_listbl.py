#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_over_crlimit_listbl():

    prepare_cache ([Hoteldpt, Htparam])

    from_dept = 1
    to_dept = 99
    depname1 = ""
    depname2 = ""
    billdate = None
    t_hoteldpt_list = []
    min_dept:int = 0
    max_dept:int = 0
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_dept, to_dept, depname1, depname2, billdate, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "billdate": billdate, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal from_dept, to_dept, depname1, depname2, billdate, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        ldry:int = 0
        dstore:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger
        min_dept = 999
        max_dept = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            if min_dept > hoteldpt.num:
                min_dept = hoteldpt.num

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num
        from_dept = min_dept
        to_dept = max_dept

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
        depname1 = hoteldpt.depart

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
        depname2 = hoteldpt.depart

    select_dept()

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0)]})

    if not hoteldpt:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()