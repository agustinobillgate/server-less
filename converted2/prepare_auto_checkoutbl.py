#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Reservation

def prepare_auto_checkoutbl(resnr:int):

    prepare_cache ([Htparam, Reservation])

    ci_date = None
    res_name = ""
    htparam = reservation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, res_name, htparam, reservation
        nonlocal resnr

        return {"ci_date": ci_date, "res_name": res_name}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:
        res_name = reservation.name

    return generate_output()