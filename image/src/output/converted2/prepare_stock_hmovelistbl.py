#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, L_artikel

def prepare_stock_hmovelistbl(s_bezeich:string, user_init:string, inp_artnr:int):

    prepare_cache ([Htparam, Bediener, L_artikel])

    price_decimal = 0
    show_price = False
    close_date = None
    mm = None
    yy = None
    fl_code = 0
    htparam = bediener = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, show_price, close_date, mm, yy, fl_code, htparam, bediener, l_artikel
        nonlocal s_bezeich, user_init, inp_artnr

        return {"s_bezeich": s_bezeich, "price_decimal": price_decimal, "show_price": show_price, "close_date": close_date, "mm": mm, "yy": yy, "fl_code": fl_code}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    if inp_artnr != 0:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, inp_artnr)]})

        if l_artikel:
            s_bezeich = l_artikel.bezeich

            if l_artikel.endkum <= 2:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
            close_date = htparam.fdate
            mm = get_month(close_date) - 1
            yy = get_year(close_date)

            if mm == 0:
                mm = 12
                yy = yy - 1


            fl_code = 1

    return generate_output()