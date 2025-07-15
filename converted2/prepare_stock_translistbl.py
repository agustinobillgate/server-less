#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, Htparam

def prepare_stock_translistbl():

    prepare_cache ([Htparam])

    avail_unter = False
    long_digit = False
    l_untergrup = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_unter, long_digit, l_untergrup, htparam

        return {"avail_unter": avail_unter, "long_digit": long_digit}


    l_untergrup = get_cache (L_untergrup, {"betriebsnr": [(eq, 1)]})
    avail_unter = None != l_untergrup

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    return generate_output()