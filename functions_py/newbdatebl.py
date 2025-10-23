#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 21-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def newbdatebl():

    prepare_cache ([Htparam])

    curr_date:date = None
    bill_date:date = None
    nbill_date:date = None
    new_date:date = None
    htparam = None

    htp = None

    Htp = create_buffer("Htp",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, bill_date, nbill_date, new_date, htparam
        nonlocal htp


        nonlocal htp

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    nbill_date = bill_date + timedelta(days=1)
    htparam.fdate = nbill_date
    pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam.fdate < nbill_date:
        pass
        htparam.fdate = nbill_date
        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 105)]})
    htparam.fdate = nbill_date
    pass

    return generate_output()