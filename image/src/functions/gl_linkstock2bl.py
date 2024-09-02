from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Counters, Gl_journal

def gl_linkstock2bl(pvilanguage:int, link_in:bool, to_date:date, remains:decimal, credits:decimal, debits:decimal, refno:str, datum:date, bezeich:str, jtype:int, g_list:[G_list]):
    new_hdr:bool = True
    lvcarea:str = "gl_linkstock"
    htparam = gl_jouhdr = counters = gl_journal = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"docu_nr":str, "lscheinnr":str, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "add_note":str, "duplicate":bool, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, gl_journal


        nonlocal g_list
        nonlocal g_list_list
        return {}

    def create_header():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, gl_journal


        nonlocal g_list
        nonlocal g_list_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters = counters + 1

        counters = db_session.query(Counters).first()
        gl_jouhdr.jnr = counters
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = jtype
        new_hdr = True

    def create_journals():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, gl_journal


        nonlocal g_list
        nonlocal g_list_list

        for g_list in query(g_list_list):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit = g_list.debit
            gl_journal.credit = g_list.credit
            gl_journal.bemerk = g_list.bemerk + g_list.add_note
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains = 0

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        gl_jouhdr.credit = credits
        gl_jouhdr.debit = debits
        gl_jouhdr.remain = remains

        gl_jouhdr = db_session.query(Gl_jouhdr).first()


    create_header()
    create_journals()

    if link_in:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1035)).first()

    if htparam.fdate < to_date:
        htparam.fdate = to_date

    htparam = db_session.query(Htparam).first()

    return generate_output()