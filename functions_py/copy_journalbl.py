#using conversion tools version: 1.0.0.117
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_journal, Gl_jouhdr, Counters
from functions.next_counter_for_update import next_counter_for_update

def copy_journalbl(desc_cj:string, credit:Decimal, debit:Decimal, remain:Decimal, jnr:int, user_init:string, datum:date, refno:string):

    prepare_cache ([Gl_journal, Gl_jouhdr, Counters])

    gl_journal = gl_jouhdr = counters = None

    gl_jnal = gl_jou = gl_hdr = None

    Gl_jnal = create_buffer("Gl_jnal",Gl_journal)
    Gl_jou = create_buffer("Gl_jou",Gl_journal)
    Gl_hdr = create_buffer("Gl_hdr",Gl_jouhdr)
    db_session = local_storage.db_session
    last_count:int = 0
    error_lock:string = ""
    desc_cj = desc_cj.strip()


    def generate_output():
        nonlocal gl_journal, gl_jouhdr, counters
        nonlocal desc_cj, credit, debit, remain, jnr, user_init, datum, refno
        nonlocal gl_jnal, gl_jou, gl_hdr


        nonlocal gl_jnal, gl_jou, gl_hdr

        return {}

    gl_hdr = Gl_jouhdr()
    db_session.add(gl_hdr)

    # Rd, 24/11/2025, get counters dengan for update
    # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
    counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 25)).with_for_update().first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 25
        counters.counter_bez = "G/L Transaction Journal"
    counters.counter = counters.counter + 1

    gl_hdr.jnr = counters.counter

    gl_hdr.refno = refno
    gl_hdr.datum = datum
    gl_hdr.bezeich = desc_cj
    gl_hdr.credit =  to_decimal(credit)
    gl_hdr.debit =  to_decimal(debit)
    gl_hdr.remain =  to_decimal(remain)
    pass

    for gl_jou in db_session.query(Gl_jou).filter(
                 (Gl_jou.jnr == jnr)).order_by(Gl_jou._recid).all():
        gl_jnal = Gl_journal()
        db_session.add(gl_jnal)

        gl_jnal.jnr = counters.counter

        gl_jnal.fibukonto = gl_jou.fibukonto
        gl_jnal.debit =  to_decimal(gl_jou.debit)
        gl_jnal.bemerk = gl_jou.bemerk
        gl_jnal.credit =  to_decimal(gl_jou.credit)
        gl_jnal.userinit = user_init
        gl_jnal.zeit = get_current_time_in_seconds()

    return generate_output()