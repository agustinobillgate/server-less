#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Waehrung

def prepare_rm_productbl():

    prepare_cache ([Htparam, Waehrung])

    price_decimal = 0
    foreign_nr = 0
    f_log = False
    htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, foreign_nr, f_log, htparam, waehrung

        return {"price_decimal": price_decimal, "foreign_nr": foreign_nr, "f_log": f_log}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    f_log = htparam.flogical

    return generate_output()