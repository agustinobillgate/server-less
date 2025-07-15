#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_pi, Counters, Gl_jouhdr, Gl_journal

def mk_gcpi_go1bbl(pvilanguage:int, docu_nr:string, billdate:date, journaltype:int, pi_acctno:string, user_init:string, pbuff_postdate:date, giro_tempacct:string):

    prepare_cache ([Gc_pi, Counters, Gl_jouhdr, Gl_journal])

    lvcarea:string = "mk-gcPI"
    gc_pi = counters = gl_jouhdr = gl_journal = None

    gc_pibuff = None

    Gc_pibuff = create_buffer("Gc_pibuff",Gc_pi)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, docu_nr, billdate, journaltype, pi_acctno, user_init, pbuff_postdate, giro_tempacct
        nonlocal gc_pibuff


        nonlocal gc_pibuff

        return {}


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    if not gc_pi:

        return generate_output()
    gc_pi.debit_fibu = pi_acctno
    gc_pi.pi_status = 1

    counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 25
        counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
    counters.counter = counters.counter + 1
    pass
    gl_jouhdr = Gl_jouhdr()
    db_session.add(gl_jouhdr)

    gl_jouhdr.jnr = counters.counter
    gl_jouhdr.jtype = journaltype
    gl_jouhdr.batch = True
    gl_jouhdr.refno = gc_pi.docu_nr
    gl_jouhdr.datum = gc_pi.pay_datum
    gl_jouhdr.bezeich = gc_pi.bemerk
    gl_jouhdr.debit =  to_decimal(gc_pi.betrag)
    gl_jouhdr.credit =  to_decimal(gc_pi.betrag)

    if gc_pi.postdate != None:
        gl_jouhdr.datum = gc_pi.postdate
    gl_journal = Gl_journal()
    db_session.add(gl_journal)

    gl_journal.jnr = counters.counter
    gl_journal.fibukonto = gc_pi.debit_fibu
    gl_journal.debit =  to_decimal(gc_pi.betrag)
    gl_journal.userinit = user_init
    gl_journal.sysdate = get_current_date()
    gl_journal.zeit = get_current_time_in_seconds()
    gl_journal.bemerk = gc_pi.bemerk


    pass
    gl_journal = Gl_journal()
    db_session.add(gl_journal)

    gl_journal.jnr = counters.counter
    gl_journal.credit =  to_decimal(gc_pi.betrag)
    gl_journal.userinit = user_init
    gl_journal.zeit = get_current_time_in_seconds()
    gl_journal.bemerk = gc_pi.bemerk

    if gc_pi.pay_type != 2 or giro_tempacct == "" or pbuff_postdate != None:
        gl_journal.fibukonto = gc_pi.credit_fibu


    else:
        gl_journal.fibukonto = giro_tempacct
    pass
    pass

    return generate_output()