from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gc_pi, Counters, Gc_pitype

def mk_gcpi_go1bl(pbuff:[Pbuff], billdate:date, rcvname:str, pi_type:str, bemerk:str, pi_acctno:str):
    pi_docuno = ""
    gc_pi = counters = gc_pitype = None

    pbuff = gc_pibuff = None

    pbuff_list, Pbuff = create_model_like(Gc_pi)

    Gc_pibuff = Gc_pi

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pi_docuno, gc_pi, counters, gc_pitype
        nonlocal gc_pibuff


        nonlocal pbuff, gc_pibuff
        nonlocal pbuff_list
        return {"pi_docuno": pi_docuno}

    def go1():

        nonlocal pi_docuno, gc_pi, counters, gc_pitype
        nonlocal gc_pibuff


        nonlocal pbuff, gc_pibuff
        nonlocal pbuff_list

        printer_nr:int = 0
        Gc_pibuff = Gc_pi
        pbuff.pay_datum = billdate

        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 42)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 42
            counters.counter_bez = "GC Proforma Invoice Counter No"

        gc_pibuff = db_session.query(Gc_pibuff).filter(
                    (substring(Gc_pibuff.docu_nr, 0, 9) == ("PI" + to_string(get_month(billdate) , "99") + to_string(get_year(billdate) , "9999") + "-"))).first()

        if not gc_pibuff:
            counters.counter = 0


        counters.counter = counters.counter + 1

        if counters.counter > 9999:
            counters.counter = 1

        counters = db_session.query(Counters).first()
        pbuff.docu_nr = "PI" + to_string(get_month(billdate) , "99") +\
                to_string(get_year(billdate) , "9999") + "-" +\
                to_string(counter.counter, "9999")
        pbuff.rcvname = rcvname

        gc_pitype = db_session.query(Gc_pitype).filter(
                    (func.lower(Gc_pitype.bezeich) == (pi_type).lower())).first()
        gc_pi = Gc_pi()
        db_session.add(gc_pi)

        buffer_copy(pbuff, gc_pi)
        pi_docuno = pbuff.docu_nr
        gc_PI.rcvname = rcvname
        gc_PI.bemerk = bemerk
        gc_PI.pi_type = gc_pitype.nr
        gc_PI.debit_fibu = pi_acctno


    pbuff = query(pbuff_list, first=True)
    go1()

    return generate_output()