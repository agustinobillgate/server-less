#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_artikel

def prepare_stock_movelistbl(s_bezeich:string, inp_artnr:int):

    prepare_cache ([Htparam, L_artikel])

    price_decimal = 0
    show_price = False
    avail_l_artikel = False
    htparam = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, show_price, avail_l_artikel, htparam, l_artikel
        nonlocal s_bezeich, inp_artnr

        return {"s_bezeich": s_bezeich, "price_decimal": price_decimal, "show_price": show_price, "avail_l_artikel": avail_l_artikel}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if inp_artnr != 0:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, inp_artnr)]})

        if l_artikel:
            s_bezeich = l_artikel.bezeich
            avail_l_artikel = True

    return generate_output()