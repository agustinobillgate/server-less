#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam

def prepare_delv_stockbl(user_init:string):

    prepare_cache ([Bediener, Htparam])

    show_price = False
    long_digit = False
    bediener = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, long_digit, bediener, htparam
        nonlocal user_init

        return {"show_price": show_price, "long_digit": long_digit}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    return generate_output()