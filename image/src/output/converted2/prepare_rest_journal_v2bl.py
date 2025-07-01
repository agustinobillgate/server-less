#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam, Queasy

def prepare_rest_journal_v2bl():

    prepare_cache ([Htparam, Queasy])

    from_date = None
    to_date = None
    long_digit = False
    min_dept = 99
    min_art = 0
    max_art = 0
    from_art = 0
    max_dept = 0
    to_art = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    avail_queasy = False
    t_queasy_list = []
    t_hoteldpt_list = []
    hoteldpt = htparam = queasy = None

    t_queasy = t_hoteldpt = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char2":string})
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, long_digit, min_dept, min_art, max_art, from_art, max_dept, to_art, from_dept, to_dept, depname1, depname2, avail_queasy, t_queasy_list, t_hoteldpt_list, hoteldpt, htparam, queasy


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_list, t_hoteldpt_list

        return {"from_date": from_date, "to_date": to_date, "long_digit": long_digit, "min_dept": min_dept, "min_art": min_art, "max_art": max_art, "from_art": from_art, "max_dept": max_dept, "to_art": to_art, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "avail_queasy": avail_queasy, "t-queasy": t_queasy_list, "t-hoteldpt": t_hoteldpt_list}

    def fill_odtaker():

        nonlocal from_date, to_date, long_digit, min_dept, min_art, max_art, from_art, max_dept, to_art, from_dept, to_dept, depname1, depname2, avail_queasy, t_queasy_list, t_hoteldpt_list, hoteldpt, htparam, queasy


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_list, t_hoteldpt_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 10)).order_by(Queasy.char2).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            t_queasy.char2 = queasy.char2

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0)]})

    if not hoteldpt:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    min_dept = 999
    max_dept = 1

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt.num).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
    depname1 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
    depname2 = hoteldpt.depart

    queasy = get_cache (Queasy, {"key": [(eq, 10)]})

    if queasy:
        avail_queasy = True
        fill_odtaker()

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()