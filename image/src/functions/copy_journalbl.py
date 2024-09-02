from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_journal, Gl_jouhdr, Counters

def copy_journalbl(desc_cj:str, credit:decimal, debit:decimal, remain:decimal, jnr:int, user_init:str, datum:date, refno:str):
    gl_journal = gl_jouhdr = counters = None

    gl_jnal = gl_jou = gl_hdr = None

    Gl_jnal = Gl_journal
    Gl_jou = Gl_journal
    Gl_hdr = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal, gl_jouhdr, counters
        nonlocal gl_jnal, gl_jou, gl_hdr


        nonlocal gl_jnal, gl_jou, gl_hdr
        return {}

    gl_hdr = Gl_hdr()
    db_session.add(gl_hdr)


    counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 25
        counters.counter_bez = "G/L Transaction Journal"
    
    counters = counters.counter + 1

    counters = db_session.query(Counters).first()
    gl_hdr.jnr = counters.counter
    gl_hdr.refno = refno
    gl_hdr.datum = datum
    gl_hdr.bezeich = desc_cj
    gl_hdr.credit = credit
    gl_hdr.debit = debit
    gl_hdr.remain = remain

    gl_hdr = db_session.query(Gl_hdr).first()

    for gl_jou in db_session.query(Gl_jou).filter(Gl_jou.jnr == jnr).all():
        gl_jnal = Gl_jnal()
        db_session.add(gl_jnal)

        gl_jnal.jnr = counters.counter
        gl_jnal.fibukonto = gl_jou.fibukonto
        gl_jnal.debit = gl_jou.debit
        gl_jnal.bemerk = gl_jou.bemerk
        gl_jnal.credit = gl_jou.credit
        gl_jnal.userinit = user_init
        gl_jnal.zeit = get_current_time_in_seconds()


    return generate_output()