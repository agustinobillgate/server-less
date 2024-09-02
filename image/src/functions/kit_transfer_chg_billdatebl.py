from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Exrate

def kit_transfer_chg_billdatebl(transdate:date, double_currency:bool, foreign_nr:int):
    exchg_rate = 0
    htparam = exrate = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, htparam, exrate


        return {"exchg_rate": exchg_rate}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam.fdate != transdate and double_currency:

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == foreign_nr and Exrate.datum == transdate)).first()
        else FIND FIRST exrate where exrate.datum = transdate

        if exrate:
            exchg_rate = exrate.betrag

    return generate_output()