#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_pi, Counters, Gl_jouhdr, Gl_journal
from functions.next_counter_for_update import next_counter_for_update

def mk_gcpi_go3bl(pvilanguage:int, docu_nr:string, pbuff_postdate:date, journaltype:int, giro_tempacct:string, user_init:string):

    prepare_cache ([Gc_pi, Counters, Gl_jouhdr, Gl_journal])

    lvcarea:string = "mk-gcPI"
    gc_pi = counters = gl_jouhdr = gl_journal = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    docu_nr = docu_nr.strip()
    user_init = user_init.strip()
    giro_tempacct = giro_tempacct.strip()

    def generate_output():
        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, docu_nr, pbuff_postdate, journaltype, giro_tempacct, user_init

        return {}

    def go3():

        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, docu_nr, pbuff_postdate, journaltype, giro_tempacct, user_init

        # gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})
        gc_pi = db_session.query(Gc_pi).filter(
                 (Gc_pi.docu_nr == docu_nr)).with_for_update().first()
        gc_pi.postdate = pbuff_postdate

        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
        counters = db_session.query(Counters).filter(Counters.counter_no == 25).with_for_update().first()

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
        gl_jouhdr.refno = gc_pi.docu_nr2 + "A"
        gl_jouhdr.datum = gc_pi.postdate
        gl_jouhdr.bezeich = gc_pi.bemerk
        gl_jouhdr.debit =  to_decimal(gc_pi.betrag)
        gl_jouhdr.credit =  to_decimal(gc_pi.betrag)


        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters.counter
        gl_journal.fibukonto = giro_tempacct
        gl_journal.debit =  to_decimal(gc_pi.betrag)
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.bemerk


        pass
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters.counter
        gl_journal.fibukonto = gc_pi.credit_fibu
        gl_journal.credit =  to_decimal(gc_pi.betrag)
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.bemerk


        pass
        pass


    go3()

    return generate_output()