#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Rmbudget

def room_budget_new_budgetbl(fdate:date, tdate:date, anzahl:int, logis:Decimal, occrm:Decimal, betrag:Decimal, user_init:string, zimkateg_zikatnr:int):

    prepare_cache ([Rmbudget])

    datum:date = None
    rmbudget = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, rmbudget
        nonlocal fdate, tdate, anzahl, logis, occrm, betrag, user_init, zimkateg_zikatnr

        return {}

    for datum in date_range(fdate,tdate) :

        if datum == tdate:
            anzahl = occrm
            logis =  to_decimal(betrag)

        rmbudget = get_cache (Rmbudget, {"datum": [(eq, datum)],"zikatnr": [(eq, zimkateg_zikatnr)]})

        if not rmbudget:
            rmbudget = Rmbudget()
            db_session.add(rmbudget)

            rmbudget.datum = datum
            rmbudget.zikatnr = zimkateg_zikatnr


        rmbudget.zimmeranz = anzahl
        rmbudget.logis =  to_decimal(logis)
        rmbudget.userinit = user_init
        rmbudget.zeit = get_current_time_in_seconds()
        occrm =  to_decimal(occrm) - to_decimal(anzahl)
        betrag =  to_decimal(betrag) - to_decimal(logis)

    return generate_output()