#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def check_gl_batchjournalbl(from_date:date, to_date:date):

    prepare_cache ([Htparam])

    avail_batch = False
    date1:date = None
    date2:date = None
    htparam = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_batch, date1, date2, htparam, gl_jouhdr
        nonlocal from_date, to_date

        return {"avail_batch": avail_batch}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    date1 = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    date2 = htparam.fdate

    if from_date > date1:
        date1 = from_date

    if to_date < date2:
        date2 = to_date

    gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, 0)],"datum": [(ge, date1),(le, date2)],"batch": [(eq, True)]})

    if gl_jouhdr:
        avail_batch = True

    return generate_output()