from functions.additional_functions import *
import decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal

def manual_arbl(pvilanguage:int, s_list:[S_list], rgdatum:date, firma:str, art_fibukonto:str, user_init:str, invoice:int, saldo:decimal, refno:str):
    lvcarea:str = "manual_ar"
    counters = gl_jouhdr = gl_journal = None

    s_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "debit":decimal, "credit":decimal}, {"fibukonto": "000000000000"})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, counters, gl_jouhdr, gl_journal
        nonlocal sbuff


        nonlocal s_list, sbuff
        nonlocal s_list_list
        return {}

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
        gl_journal.debit = saldo
    else:
        gl_journal.credit = - saldo
    gl_jouhdr.credit = gl_jouhdr.credit + gl_journal.credit
    gl_jouhdr.debit = gl_jouhdr.debit + gl_journal.debit

    for sbuff in query(sbuff_list, filters=(lambda sbuff :decimal.Decimal(sbuff.fibukonto) != 0)):
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.fibukonto = sbuff.fibukonto
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = to_string(invoice)
        gl_journal.debit = sbuff.debit
        gl_journal.credit = sbuff.credit


        gl_jouhdr.credit = gl_jouhdr.credit + gl_journal.credit
        gl_jouhdr.debit = gl_jouhdr.debit + gl_journal.debit

        gl_journal = db_session.query(Gl_journal).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).first()

    return generate_output()