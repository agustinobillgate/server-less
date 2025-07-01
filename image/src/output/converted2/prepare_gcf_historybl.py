#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam

def prepare_gcf_historybl(gastnr:int):

    prepare_cache ([Guest, Htparam])

    fdate = None
    t_tittle = ""
    guest = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, t_tittle, guest, htparam
        nonlocal gastnr

        return {"fdate": fdate, "t_tittle": t_tittle}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        t_tittle = t_tittle + " - " + (guest.name + ", " + guest.vorname1 + guest.anredefirma)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    fdate = htparam.fdate

    return generate_output()