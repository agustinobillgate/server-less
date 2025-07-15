#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Waehrung, Htparam

def prepare_rm_fproductbl():

    prepare_cache ([Waehrung, Htparam])

    bfast_art = 0
    lunch_art = 0
    dinner_art = 0
    lundin_art = 0
    local_curr = 0
    new_contrate = False
    curr_date = None
    double_currency = False
    exchg_rate = to_decimal("0.0")
    price_decimal = 0
    waehrung = htparam = None

    wrung = None

    Wrung = create_buffer("Wrung",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bfast_art, lunch_art, dinner_art, lundin_art, local_curr, new_contrate, curr_date, double_currency, exchg_rate, price_decimal, waehrung, htparam
        nonlocal wrung


        nonlocal wrung

        return {"bfast_art": bfast_art, "lunch_art": lunch_art, "dinner_art": dinner_art, "lundin_art": lundin_art, "local_curr": local_curr, "new_contrate": new_contrate, "curr_date": curr_date, "double_currency": double_currency, "exchg_rate": exchg_rate, "price_decimal": price_decimal}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
    lundin_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    wrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
    local_curr = wrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    return generate_output()