from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Exrate

def ts_restinv_checkbl(exchg_rate:decimal, transdate:date, double_currency:bool):
    htparam = exrate = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, exrate


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam.fdate != transdate and double_currency:

        exrate = db_session.query(Exrate).filter(
                (Exrate.datum == transdate)).first()

        if exrate:
            exchg_rate = exrate.betrag

    return generate_output()