from functions.additional_functions import *
import decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal

def gl_xlsjourn_post_itbl(g_list:[G_list], pvilanguage:int, datum:date, journ_no:str, jour_type:int, journ_name:str, debits:decimal, credits:decimal, remains:decimal):
    t_jnr = 0
    lvcarea:str = "gl_xlsjourn"
    counters = gl_jouhdr = gl_journal = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "fibukonto2":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bemerk":str, "descr":str, "duplicate":bool, "correct":int}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_jnr, lvcarea, counters, gl_jouhdr, gl_journal


        nonlocal g_list
        nonlocal g_list_list
        return {"t_jnr": t_jnr}

    def post_it():

        nonlocal t_jnr, lvcarea, counters, gl_jouhdr, gl_journal


        nonlocal g_list
        nonlocal g_list_list

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
        gl_jouhdr.refno = journ_no
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = journ_name
        gl_jouhdr.jtype = jour_type
        gl_jouhdr.credit = credits
        gl_jouhdr.debit = debits
        gl_jouhdr.remain = remains
        gl_jouhdr.BATCH = True

        if jour_type == 0:
            gl_jouhdr.BATCH = False

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        t_jnr = gl_jouhdr.jnr

        for g_list in query(g_list_list):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters
            gl_journal.fibukonto = g_list.fibukonto2
            gl_journal.debit = g_list.debit
            gl_journal.credit = g_list.credit
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit
            gl_journal.bemerk = g_list.bemerk

    post_it()

    return generate_output()