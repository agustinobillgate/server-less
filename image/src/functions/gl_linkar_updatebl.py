from functions.additional_functions import *
import decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal, Htparam

def gl_linkar_updatebl(pvilanguage:int, remains:decimal, credits:decimal, debits:decimal, to_date:date, c_refno:str, c_bezeich:str, datum:date, g_list:[G_list]):
    new_hdr:bool = True
    curr_counter:int = 0
    lvcarea:str = "gl_linkar"
    counters = gl_jouhdr = gl_journal = htparam = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "add_info":str, "counter":int, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam


        nonlocal g_list
        nonlocal g_list_list
        return {}

    def create_header():

        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam


        nonlocal g_list
        nonlocal g_list_list

        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25


            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters.counter = counters.counter + 1
        curr_counter = counters.counter

        counters = db_session.query(Counters).first()
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = curr_counter
        gl_jouhdr.refno = c_refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = c_bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 2
        new_hdr = True

        gl_jouhdr = db_session.query(Gl_jouhdr).first()


    def create_journals():

        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam


        nonlocal g_list
        nonlocal g_list_list

        for g_list in query(g_list_list, filters=(lambda g_list :(round(g_list.debit, 2) != 0 or round(g_list.credit, 2) != 0))):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = curr_counter
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit = g_list.debit
            gl_journal.credit = g_list.credit
            gl_journal.bemerk = g_list.bemerk + g_list.add_info
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains = 0

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        gl_jouhdr.credit = credits
        gl_jouhdr.debit = debits
        gl_jouhdr.remain = remains

        gl_jouhdr = db_session.query(Gl_jouhdr).first()


        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1014)).first()
        htparam.fdate = datum

        htparam = db_session.query(Htparam).first()

    create_header()
    create_journals()

    return generate_output()