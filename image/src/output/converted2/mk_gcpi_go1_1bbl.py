#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_giro

def mk_gcpi_go1_1bbl(chequeno:string, duedate:date, postdate:date, pay_amount:Decimal, docu_nr:string):

    prepare_cache ([Gc_giro])

    gc_giro = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_giro
        nonlocal chequeno, duedate, postdate, pay_amount, docu_nr

        return {}


    gc_giro = get_cache (Gc_giro, {"gironum": [(eq, chequeno)]})

    if gc_giro:
        gc_giro.giro_status = 1
        gc_giro.duedate = duedate
        gc_giro.posteddate = postdate
        gc_giro.betrag =  to_decimal(pay_amount)
        gc_giro.docu_nr = docu_nr


        pass
        pass

    return generate_output()