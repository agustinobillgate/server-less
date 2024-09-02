from functions.additional_functions import *
import decimal
from datetime import date
from models import Rmbudget

def room_budget_new_budgetbl(fdate:date, tdate:date, anzahl:int, logis:decimal, occrm:decimal, betrag:decimal, user_init:str, zimkateg_zikatnr:int):
    datum:date = None
    rmbudget = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, rmbudget


        return {}

    for datum in range(fdate,tdate + 1) :

        if datum == tdate:
            anzahl = occrm
            logis = betrag

        rmbudget = db_session.query(Rmbudget).filter(
                (Rmbudget.datum == datum) &  (Rmbudget.zikatnr == zimkateg_zikatnr)).first()

        if not rmbudget:
            rmbudget = Rmbudget()
            db_session.add(rmbudget)

            rmbudget.datum = datum
            rmbudget.zikatnr = zimkateg_zikatnr


        rmbudget.zimmeranz = anzahl
        rmbudget.logis = logis
        rmbudget.userinit = user_init
        rmbudget.zeit = get_current_time_in_seconds()
        occrm = occrm - anzahl
        betrag = betrag - logis

    return generate_output()