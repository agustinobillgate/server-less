#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_pi, Counters, Gc_pitype
from functions.next_counter_for_update import next_counter_for_update

pbuff_data, Pbuff = create_model_like(Gc_pi)

def mk_gcpi_go1bl(pbuff_data:[Pbuff], billdate:date, rcvname:string, pi_type:string, bemerk:string, pi_acctno:string):

    prepare_cache ([Gc_pi, Counters, Gc_pitype])

    pi_docuno = ""
    gc_pi = counters = gc_pitype = None

    pbuff = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    rcvname = rcvname.strip()
    pi_type = pi_type.strip()
    bemerk = bemerk.strip()
    pi_acctno = pi_acctno.strip()

    def generate_output():
        nonlocal pi_docuno, gc_pi, counters, gc_pitype
        nonlocal billdate, rcvname, pi_type, bemerk, pi_acctno


        nonlocal pbuff

        return {"pbuff": pbuff_data, "pi_docuno": pi_docuno}

    def go1():

        nonlocal pi_docuno, gc_pi, counters, gc_pitype
        nonlocal billdate, rcvname, pi_type, bemerk, pi_acctno


        nonlocal pbuff

        printer_nr:int = 0
        gc_pibuff = None
        Gc_pibuff =  create_buffer("Gc_pibuff",Gc_pi)
        pbuff.pay_datum = billdate

        # counters = get_cache (Counters, {"counter_no": [(eq, 42)]})
        counters = db_session.query(Counters).filter(Counters.counter_no == 42).with_for_update().first()
        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 42
            counters.counter_bez = "GC Proforma Invoice Counter No"

        gc_pibuff = db_session.query(Gc_pibuff).filter(
                     (substring(Gc_pibuff.docu_nr, 0, 9) == (("PI" + to_string(get_month(billdate) , "99") + to_string(get_year(billdate) , "9999") + "-").lower()))).first()

        if not gc_pibuff:
            counters.counter = 0


        counters.counter = counters.counter + 1

        if counters.counter > 9999:
            counters.counter = 1
        pass
        pbuff.docu_nr = "PI" + to_string(get_month(billdate) , "99") +\
                to_string(get_year(billdate) , "9999") + "-" +\
                to_string(counters.counter, "9999")
        pbuff.rcvname = rcvname

        gc_pitype = get_cache (Gc_pitype, {"bezeich": [(eq, pi_type)]})
        gc_pi = Gc_pi()
        db_session.add(gc_pi)

        buffer_copy(pbuff, gc_pi)
        pi_docuno = pbuff.docu_nr
        gc_pi.rcvname = rcvname
        gc_pi.bemerk = bemerk
        gc_pi.pi_type = gc_pitype.nr
        gc_pi.debit_fibu = pi_acctno


    pbuff = query(pbuff_data, first=True)
    go1()

    return generate_output()