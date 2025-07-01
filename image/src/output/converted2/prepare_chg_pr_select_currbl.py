#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Waehrung

def prepare_chg_pr_select_currbl():

    prepare_cache ([Htparam, Waehrung])

    t_currency_list = []
    htparam = waehrung = None

    t_currency = None

    t_currency_list, T_currency = create_model("T_currency", {"currnr":int, "currid":string, "exrate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_currency_list, htparam, waehrung


        nonlocal t_currency
        nonlocal t_currency_list

        return {"t-currency": t_currency_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        t_currency = T_currency()
        t_currency_list.append(t_currency)

        t_currency.currnr = waehrung.waehrungsnr
        t_currency.currid = waehrung.wabkurz
        t_currency.exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    for waehrung in db_session.query(Waehrung).filter(
             (Waehrung.wabkurz != htparam.fchar) & (Waehrung.ankauf > 0)).order_by(Waehrung.wabkurz).all():
        t_currency = T_currency()
        t_currency_list.append(t_currency)

        t_currency.currnr = waehrung.waehrungsnr
        t_currency.currid = waehrung.wabkurz
        t_currency.exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    return generate_output()