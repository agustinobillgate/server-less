#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_rest_rsvplanbl():

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    min_dept = 99
    max_dept = 0
    from_dept = 0
    to_dept = 0
    curr_dept = 0
    depname1 = ""
    depname2 = ""
    depname3 = ""
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, min_dept, max_dept, from_dept, to_dept, curr_dept, depname1, depname2, depname3, t_hoteldpt_list, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"from_date": from_date, "to_date": to_date, "min_dept": min_dept, "max_dept": max_dept, "from_dept": from_dept, "to_dept": to_dept, "curr_dept": curr_dept, "depname1": depname1, "depname2": depname2, "depname3": depname3, "t-hoteldpt": t_hoteldpt_list}

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0)]})

    if not hoteldpt:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = htparam.fdate
    min_dept = 999
    max_dept = 1

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt.num).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    curr_dept = min_dept
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
    depname1 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
    depname2 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
    depname3 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()