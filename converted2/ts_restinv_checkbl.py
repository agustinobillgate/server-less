#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Exrate

def ts_restinv_checkbl(exchg_rate:Decimal, transdate:date, double_currency:bool):

    prepare_cache ([Htparam, Exrate])

    htparam = exrate = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, exrate
        nonlocal exchg_rate, transdate, double_currency

        return {"exchg_rate": exchg_rate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam.fdate != transdate and double_currency:

        exrate = get_cache (Exrate, {"datum": [(eq, transdate)]})

        if exrate:
            exchg_rate =  to_decimal(exrate.betrag)

    return generate_output()