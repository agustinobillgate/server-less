from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gc_pi, Counters, Gl_jouhdr, Gl_journal

def mk_gcpi_go2abl(pvilanguage:int, journaltype:int, pbuff_betrag:decimal, pbuff_returnamt:decimal, ret_acctno:str, user_init:str, docu_nr:str, inv_list:[Inv_list]):
    lvcarea:str = "mk_gcPI"
    gc_pi = counters = gl_jouhdr = gl_journal = None

    inv_list = None

    inv_list_list, Inv_list = create_model("Inv_list", {"s_recid":int, "reihenfolge":int, "amount":decimal, "remark":str, "inv_acctno":str, "inv_bezeich":str, "supplier":str, "invno":str, "created":date, "zeit":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, gc_pi, counters, gl_jouhdr, gl_journal


        nonlocal inv_list
        nonlocal inv_list_list
        return {}

    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()

    gc_pi = db_session.query(Gc_pi).first()

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
    gl_jouhdr.refno = gc_pi.docu_nr2
    gl_jouhdr.datum = gc_pi.datum2
    gl_jouhdr.bezeich = gc_pi.docu_nr

    if pbuff_returnamt < 0:
        gl_jouhdr.debit = pbuff_betrag - pbuff_returnamt
        gl_jouhdr.credit = pbuff_betrag - pbuff_returnamt


    else:
        gl_jouhdr.debit = pbuff_betrag
        gl_jouhdr.credit = pbuff_betrag

    if pbuff_returnamt != 0:
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters
        gl_journal.fibukonto = ret_acctno
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gc_pi.docu_nr

        if pbuff_returnamt > 0:
            gl_journal.debit = pbuff_returnamt
        else:
            gl_journal.credit = - pbuff_returnamt

        gl_journal = db_session.query(Gl_journal).first()
    gl_journal = Gl_journal()
    db_session.add(gl_journal)

    gl_journal.jnr = counters
    gl_journal.fibukonto = gc_PI.debit_fibu
    gl_journal.credit = gc_pi.betrag
    gl_journal.userinit = user_init
    gl_journal.sysdate = get_current_date()
    gl_journal.zeit = get_current_time_in_seconds()
    gl_journal.bemerk = gc_pi.docu_nr

    gl_journal = db_session.query(Gl_journal).first()

    for inv_list in query(inv_list_list):
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = counters
        gl_journal.fibukonto = inv_list.inv_acctNo
        gl_journal.debit = inv_list.amount
        gl_journal.userinit = user_init
        gl_journal.sysdate = get_current_date()
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = inv_list.remark

        if inv_list.supplier != "" or inv_list.invNo != "":
            gl_journal.bemerk = gl_journal.bemerk + " [" + inv_list.supplier + "-" + inv_list.invNo + "]"

        gl_journal = db_session.query(Gl_journal).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).first()
    gc_pi.pi_status = 2

    gc_pi = db_session.query(Gc_pi).first()


    return generate_output()