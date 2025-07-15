#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bediener

def prepare_chg_storerequestbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    show_price = False
    req_flag = False
    p_220 = 0
    htparam = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, p_220, htparam, bediener
        nonlocal user_init

        return {"show_price": show_price, "req_flag": req_flag, "p_220": p_220}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

    if htparam:
        show_price = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        if substring(bediener.permissions, 21, 1) != ("0").lower() :
            show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 475)]})

    if htparam:
        req_flag = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 220)]})

    if htparam:
        p_220 = htparam.finteger

    return generate_output()