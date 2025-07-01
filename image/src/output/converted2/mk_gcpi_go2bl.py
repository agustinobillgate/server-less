#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Counters, Gc_pi

def mk_gcpi_go2bl(pi_number:string, billdate:date):

    prepare_cache ([Counters, Gc_pi])

    pbuff_docu_nr2 = ""
    printed2 = False
    counters = gc_pi = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pbuff_docu_nr2, printed2, counters, gc_pi
        nonlocal pi_number, billdate

        return {"pbuff_docu_nr2": pbuff_docu_nr2, "printed2": printed2}


    counters = get_cache (Counters, {"counter_no": [(eq, 43)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 43
        counters.counter_bez = "GC Proforma Invoice SETTLEMENT Counter No"


    counters.counter = counters.counter + 1

    if counters.counter > 9999:
        counters.counter = 1
    pass
    pbuff_docu_nr2 = "IS" + to_string(get_month(billdate) , "99") +\
            to_string(get_year(billdate) , "9999") + "-" +\
            to_string(counters.counter, "9999")

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, pi_number)]})

    if gc_pi:
        pass
        gc_pi.docu_nr2 = pbuff_docu_nr2


        pass
        printed2 = gc_pi.printed2
        pass

    return generate_output()