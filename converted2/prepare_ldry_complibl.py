#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung

def prepare_ldry_complibl():

    prepare_cache ([Htparam, Waehrung])

    billdate = None
    from_dept = 0
    double_currency = False
    foreign_nr = 0
    exchg_rate = to_decimal("0.0")
    htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, from_dept, double_currency, foreign_nr, exchg_rate, htparam, waehrung

        return {"billdate": billdate, "from_dept": from_dept, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    from_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam.flogical:
        double_currency = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")

    return generate_output()