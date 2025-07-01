#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def prepare_gl_jourefbl():

    prepare_cache ([Htparam, Gl_jouhdr])

    from_date = None
    to_date = None
    from_refno = ""
    ref_bez = ""
    htparam = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, from_refno, ref_bez, htparam, gl_jouhdr

        return {"from_date": from_date, "to_date": to_date, "from_refno": from_refno, "ref_bez": ref_bez}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    from_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    to_date = get_current_date()

    gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(eq, from_date)]})

    if gl_jouhdr:
        from_refno = gl_jouhdr.refno
        ref_bez = gl_jouhdr.bezeich

    return generate_output()