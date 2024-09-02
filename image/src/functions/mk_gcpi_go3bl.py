from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gc_pi, Counters, Gl_jouhdr, Gl_journal

def mk_gcpi_go3bl(pvilanguage:int, docu_nr:str, pbuff_postdate:date, journaltype:int, giro_tempacct:str, user_init:str):
    lvcarea:str = "mk_gcPI"
    gc_pi = counters = gl_jouhdr = gl_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal


        return {}

    def go3():

        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal

        gc_pi = db_session.query(Gc_pi).filter(
                (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()
        gc_pi.postDate = pbuff_postdate

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters = counters + 1

        counters = db_session.query(Counters).first()
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = counters
        gl_jouhdr.jtype = journaltype
        gl_jouhdr.BATCH = True
        gl_jouhdr.refno = gc_pi.docu_nr2 + "A"
        gl_jouhdr.datum = gc_pi.postDate
        gl_jouhdr.bezeich = gc_pi.bemerk
        gl_jouhdr.debit = gc_pi.betrag
        gl_jouhdr.credit = gc_pi.betrag


        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters
        gl_journal.fibukonto = giro_tempacct
        gl_journal.debit = gc_pi.betrag
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.bemerk

        gl_journal = db_session.query(Gl_journal).first()
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters
        gl_journal.fibukonto = gc_PI.credit_fibu
        gl_journal.credit = gc_pi.betrag
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.bemerk

        gl_journal = db_session.query(Gl_journal).first()

        gl_jouhdr = db_session.query(Gl_jouhdr).first()

    go3()

    return generate_output()