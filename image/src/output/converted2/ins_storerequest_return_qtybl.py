#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Htparam

def ins_storerequest_return_qtybl(s_artnr:int, qty:Decimal, stock_oh:Decimal):

    prepare_cache ([L_artikel])

    err_flag = 0
    l_artikel = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, l_artikel, htparam
        nonlocal s_artnr, qty, stock_oh

        return {"err_flag": err_flag}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if qty > stock_oh and l_artikel.betriebsnr == 0:
        err_flag = 1

        return generate_output()
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 232)]})

        if htparam.flogical:
            err_flag = 2

            return generate_output()
        else:
            err_flag = 99

    return generate_output()