#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal
from functions.next_counter_for_update import next_counter_for_update

s_list_data, S_list = create_model("S_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal}, {"fibukonto": "000000000000"})

def manual_arbl(pvilanguage:int, s_list_data:[S_list], rgdatum:date, firma:string, art_fibukonto:string, user_init:string, invoice:int, saldo:Decimal, refno:string):

    prepare_cache ([Counters, Gl_jouhdr, Gl_journal])

    lvcarea:string = "manual-ar"
    counters = gl_jouhdr = gl_journal = None

    s_list = sbuff = None

    Sbuff = S_list
    sbuff_data = s_list_data

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    firma = firma.strip()
    art_fibukonto = art_fibukonto.strip()
    refno = refno.strip()



    def generate_output():
        nonlocal lvcarea, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, rgdatum, firma, art_fibukonto, user_init, invoice, saldo, refno
        nonlocal sbuff


        nonlocal s_list, sbuff

        return {}

    counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 25
        counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")

    # counters.counter = counters.counter + 1
    last_count, error_lock = get_output(next_counter_for_update(25))
    
    gl_jouhdr = Gl_jouhdr()
    db_session.add(gl_jouhdr)

    # gl_jouhdr.jnr = counters.counter
    gl_jouhdr.jnr = last_count

    gl_jouhdr.refno = refno
    gl_jouhdr.datum = rgdatum
    gl_jouhdr.bezeich = firma
    gl_jouhdr.batch = True
    gl_jouhdr.jtype = 2


    gl_journal = Gl_journal()
    db_session.add(gl_journal)

    gl_journal.jnr = gl_jouhdr.jnr
    gl_journal.fibukonto = art_fibukonto
    gl_journal.userinit = user_init
    gl_journal.zeit = get_current_time_in_seconds()
    gl_journal.bemerk = to_string(invoice)

    if saldo > 0:
        gl_journal.debit =  to_decimal(saldo)
    else:
        gl_journal.credit =  - to_decimal(saldo)
    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(gl_journal.credit)
    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(gl_journal.debit)

    for sbuff in query(sbuff_data, filters=(lambda sbuff: to_decimal(sbuff.fibukonto) != 0)):
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.fibukonto = sbuff.fibukonto
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = to_string(invoice)
        gl_journal.debit =  to_decimal(sbuff.debit)
        gl_journal.credit =  to_decimal(sbuff.credit)


        gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(gl_journal.credit)
        gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(gl_journal.debit)
        pass
    pass

    return generate_output()