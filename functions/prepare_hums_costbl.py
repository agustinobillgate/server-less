#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung

def prepare_hums_costbl():

    prepare_cache ([Htparam, Waehrung])

    to_date = None
    from_date = None
    double_currency = False
    foreign_nr = 0
    exchg_rate = 1
    htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, from_date, double_currency, foreign_nr, exchg_rate, htparam, waehrung

        return {"to_date": to_date, "from_date": from_date, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    return generate_output()