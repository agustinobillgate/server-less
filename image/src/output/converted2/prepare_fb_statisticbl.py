#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_fb_statisticbl(fdept:int, tdept:int):

    prepare_cache ([Htparam])

    price_decimal = 0
    ci_date = None
    fdpt_str = ""
    tdpt_str = ""
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, ci_date, fdpt_str, tdpt_str, t_hoteldpt_list, hoteldpt, htparam
        nonlocal fdept, tdept


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"price_decimal": price_decimal, "ci_date": ci_date, "fdpt_str": fdpt_str, "tdpt_str": tdpt_str, "t-hoteldpt": t_hoteldpt_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0),(eq, fdept)]})

    if hoteldpt:
        fdpt_str = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0),(eq, tdept)]})

    if hoteldpt:
        tdpt_str = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()