#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from models import Htparam, H_artikel

def prepare_ts_cash1bl(dept:int):

    prepare_cache ([Htparam])

    c_param870 = ""
    double_currency = False
    voucher_found = False
    htparam = h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_param870, double_currency, voucher_found, htparam, h_artikel
        nonlocal dept

        return {"c_param870": c_param870, "double_currency": double_currency, "voucher_found": voucher_found}

    c_param870 = get_output(htpchar(870))
    double_currency = get_output(htplogic(240))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})

    if htparam.finteger > 0:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})
        voucher_found = None != h_artikel

    return generate_output()