#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Waehrung, Hoteldpt

def prepare_quick_postbl():

    prepare_cache ([Htparam, Waehrung, Hoteldpt])

    foreign_rate = False
    double_currency = False
    price_decimal = 0
    exchg_rate = to_decimal("0.0")
    curr_local = ""
    curr_foreign = ""
    t_hoteldpt_list = []
    htparam = waehrung = hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal foreign_rate, double_currency, price_decimal, exchg_rate, curr_local, curr_foreign, t_hoteldpt_list, htparam, waehrung, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"foreign_rate": foreign_rate, "double_currency": double_currency, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "t-hoteldpt": t_hoteldpt_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num

    return generate_output()