#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam

def prepare_expired_polistbl(user_init:string):

    prepare_cache ([Bediener, Htparam])

    show_price = None
    bediener = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, bediener, htparam
        nonlocal user_init

        return {"show_price": show_price}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    return generate_output()