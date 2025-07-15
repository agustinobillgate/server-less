#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Genstat, Queasy

def prepare_nt_tauziarptbl():

    prepare_cache ([Htparam, Queasy])

    curr_date = None
    curr_month = 0
    curr_year = 0
    linkgsheet = ""
    linkgsheet1 = ""
    linkgsheet2 = ""
    htparam = genstat = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, curr_month, curr_year, linkgsheet, linkgsheet1, linkgsheet2, htparam, genstat, queasy

        return {"curr_date": curr_date, "curr_month": curr_month, "curr_year": curr_year, "linkgsheet": linkgsheet, "linkgsheet1": linkgsheet1, "linkgsheet2": linkgsheet2}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if get_day(htparam.fdate) == 1:
        curr_date = htparam.fDate
    else:

        genstat = get_cache (Genstat, {"datum": [(eq, htparam.fdate)]})

        if genstat:
            curr_date = htparam.fDate
        else:
            curr_date = htparam.fDate - timedelta(days=1)
    curr_month = get_month(curr_date)
    curr_year = get_year(curr_date)

    queasy = get_cache (Queasy, {"key": [(eq, 193)],"char1": [(eq, "tauziarpt - occfcast")]})

    if queasy:
        linkgsheet = queasy.char2

    queasy = get_cache (Queasy, {"key": [(eq, 193)],"char1": [(eq, "tauziarpt - guestrpt")]})

    if queasy:
        linkgsheet1 = queasy.char2

    queasy = get_cache (Queasy, {"key": [(eq, 193)],"char1": [(eq, "tauziarpt - revenuerpt")]})

    if queasy:
        linkgsheet2 = queasy.char1

    return generate_output()