#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam

def na_update171():

    prepare_cache ([Queasy, Htparam])

    ci_date:date = None
    queasy = htparam = None

    qsy = None

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, queasy, htparam
        nonlocal qsy


        nonlocal qsy

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        ci_date = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, ci_date)],"logi2": [(eq, False)],"logi1": [(eq, False)]})
    while None != queasy:

        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

        if qsy:
            qsy.logi2 = True


            pass
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 == ci_date) & (Queasy.logi2 == False) & (Queasy.logi1 == False) & (Queasy._recid > curr_recid)).first()

    return generate_output()