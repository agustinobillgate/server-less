#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam

def mn_chg_sysdatesbl():

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam

        return {}

    def chg_sysdates():
        nonlocal htparam
        curr_date:date = None
        new_date:date = None
        htp = None
        Htp =  create_buffer("Htp",Htparam)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})

        if (htparam.fdate + timedelta(days=1)) <= get_current_date():
            pass
            htparam.fdate = htparam.fdate + timedelta(days=1)
            pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})
        curr_date = htparam.fdate
        new_date = curr_date + timedelta(days=1)

        htp = get_cache (Htparam, {"paramnr": [(eq, 597)]})

        if curr_date > htp.fdate:
            curr_date = htp.fdate
        htparam.fdate = new_date
        pass


    chg_sysdates()

    return generate_output()