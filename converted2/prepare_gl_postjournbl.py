#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, L_lieferant

def prepare_gl_postjournbl(adjust_flag:bool):

    prepare_cache ([Htparam])

    f_int = 0
    datum = None
    last_acctdate = None
    acct_date = None
    close_year = None
    avail_queasy = False
    gst_flag = False
    htparam = queasy = l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, datum, last_acctdate, acct_date, close_year, avail_queasy, gst_flag, htparam, queasy, l_lieferant
        nonlocal adjust_flag

        return {"f_int": f_int, "datum": datum, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "avail_queasy": avail_queasy, "gst_flag": gst_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    if not adjust_flag:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    datum = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acctdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 108)]})

    if not queasy:
        avail_queasy = False
    else:
        avail_queasy = True

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()