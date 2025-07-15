#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest, Bediener

def sls_checkaccright(gastno:int):

    prepare_cache ([Htparam, Guest, Bediener])

    restriction = False
    gcf_restrict:bool = False
    shared = None
    htparam = guest = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal restriction, gcf_restrict, shared, htparam, guest, bediener
        nonlocal gastno

        return {"restriction": restriction}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1202)]})
    gcf_restrict = htparam.flogical

    if not gcf_restrict:

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

    if not guest:

        return generate_output()

    if guest.phonetik3 == user_init or guest.phonetik3 == "":

        return generate_output()
    else:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if substring(bediener.permissions, 31, 1) < ("2").lower() :
            restriction = True

    return generate_output()