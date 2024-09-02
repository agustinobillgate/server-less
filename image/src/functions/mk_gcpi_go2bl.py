from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gc_pi, Counters

def mk_gcpi_go2bl(pi_number:str, billdate:date):
    pbuff_docu_nr2 = ""
    printed2 = False
    gc_pi = counters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pbuff_docu_nr2, printed2, gc_pi, counters


        return {"pbuff_docu_nr2": pbuff_docu_nr2, "printed2": printed2}


    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.docu_nr) == (pi_number).lower())).first()

    counters = db_session.query(Counters).filter(
            (Counters.counter_no == 43)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 43
        counters.counter_bez = "GC Proforma Invoice SETTLEMENT Counter No"


    counters.counter = counters.counter + 1

    if counters.counter > 9999:
        counters.counter = 1

    counters = db_session.query(Counters).first()
    pbuff_docu_nr2 = "IS" + to_string(get_month(billdate) , "99") +\
            to_string(get_year(billdate) , "9999") + "-" +\
            to_string(counter.counter, "9999")

    gc_pi = db_session.query(Gc_pi).first()
    gc_pi.docu_nr2 = pbuff_docu_nr2

    gc_pi = db_session.query(Gc_pi).first()
    printed2 = gc_pi.printed2

    return generate_output()