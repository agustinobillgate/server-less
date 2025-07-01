#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Exrate

def kit_transfer_chg_billdatebl(transdate:date, double_currency:bool, foreign_nr:int):

    prepare_cache ([Htparam, Exrate])

    exchg_rate = 1
    htparam = exrate = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, htparam, exrate
        nonlocal transdate, double_currency, foreign_nr

        return {"exchg_rate": exchg_rate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam.fdate != transdate and double_currency:

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, transdate)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, transdate)]})

        if exrate:
            exchg_rate =  to_decimal(exrate.betrag)

    return generate_output()