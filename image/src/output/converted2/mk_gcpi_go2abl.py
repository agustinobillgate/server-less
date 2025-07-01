#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_pi, Counters, Gl_jouhdr, Gl_journal

inv_list_list, Inv_list = create_model("Inv_list", {"s_recid":int, "reihenfolge":int, "amount":Decimal, "remark":string, "inv_acctno":string, "inv_bezeich":string, "supplier":string, "invno":string, "created":date, "zeit":int})

def mk_gcpi_go2abl(pvilanguage:int, journaltype:int, pbuff_betrag:Decimal, pbuff_returnamt:Decimal, ret_acctno:string, user_init:string, docu_nr:string, inv_list_list:[Inv_list]):

    prepare_cache ([Gc_pi, Counters, Gl_jouhdr, Gl_journal])

    lvcarea:string = "mk-gcPI"
    gc_pi = counters = gl_jouhdr = gl_journal = None

    inv_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, journaltype, pbuff_betrag, pbuff_returnamt, ret_acctno, user_init, docu_nr


        nonlocal inv_list

        return {}

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})
    pass

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
    gl_jouhdr.refno = gc_pi.docu_nr2
    gl_jouhdr.datum = gc_pi.datum2
    gl_jouhdr.bezeich = gc_pi.docu_nr

    if pbuff_returnamt < 0:
        gl_jouhdr.debit =  to_decimal(pbuff_betrag) - to_decimal(pbuff_returnamt)
        gl_jouhdr.credit =  to_decimal(pbuff_betrag) - to_decimal(pbuff_returnamt)


    else:
        gl_jouhdr.debit =  to_decimal(pbuff_betrag)
        gl_jouhdr.credit =  to_decimal(pbuff_betrag)

    if pbuff_returnamt != 0:
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters.counter
        gl_journal.fibukonto = ret_acctno
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.docu_nr

        if pbuff_returnamt > 0:
            gl_journal.debit =  to_decimal(pbuff_returnamt)
        else:
            gl_journal.credit =  - to_decimal(pbuff_returnamt)
        pass
    gl_journal = Gl_journal()
    db_session.add(gl_journal)

    gl_journal.jnr = counters.counter
    gl_journal.fibukonto = gc_pi.debit_fibu
    gl_journal.credit =  to_decimal(gc_pi.betrag)
    gl_journal.userinit = user_init
    gl_journal.sysdate = get_current_date()
    gl_journal.zeit = get_current_time_in_seconds()
    gl_journal.bemerk = gc_pi.docu_nr


    pass

    for inv_list in query(inv_list_list):
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters.counter
        gl_journal.fibukonto = inv_list.inv_acctNo
        gl_journal.debit =  to_decimal(inv_list.amount)
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = inv_list.remark

        if inv_list.supplier != "" or inv_list.invNo != "":
            gl_journal.bemerk = gl_journal.bemerk
        pass
    pass
    gc_pi.pi_status = 2


    pass

    return generate_output()