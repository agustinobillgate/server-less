#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_copy_journalbl():

    prepare_cache ([Htparam])

    last_acctdate = None
    datum = None
    fl_temp = False
    finteger = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_acctdate, datum, fl_temp, finteger, htparam

        return {"last_acctdate": last_acctdate, "datum": datum, "fl_temp": fl_temp, "finteger": finteger}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acctdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})
    datum = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        fl_temp = True
        finteger = htparam.finteger

    return generate_output()