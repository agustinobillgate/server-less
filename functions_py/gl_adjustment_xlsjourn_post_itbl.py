#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "fibukonto2":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "bemerk":string, "descr":string, "duplicate":bool, "correct":int}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_adjustment_xlsjourn_post_itbl(g_list_data:[G_list], pvilanguage:int, datum:date, journ_no:string, 
                                     jour_type:int, journ_name:string, debits:[Decimal], credits:[Decimal], remains:[Decimal]):

    prepare_cache ([Counters, Gl_jouhdr, Gl_journal])

    t_jnr = 0
    lvcarea:string = "gl-xlsjourn"
    counters = gl_jouhdr = gl_journal = None

    g_list = None

    db_session = local_storage.db_session
    journ_no = journ_no.strip()
    journ_name = journ_name.strip()


    def generate_output():
        nonlocal t_jnr, lvcarea, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, datum, journ_no, jour_type, journ_name


        nonlocal g_list

        return {"t_jnr": t_jnr}

    def post_it():

        nonlocal t_jnr, lvcarea, counters, gl_jouhdr, gl_journal
        nonlocal pvilanguage, datum, journ_no, jour_type, journ_name


        nonlocal g_list

        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
        counters = db_session.query(Counters).filter(Counters.counter_no == 25).with_for_update().first()

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
        
        gl_jouhdr.refno = journ_no
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = journ_name
        gl_jouhdr.jtype = jour_type
        gl_jouhdr.credit =  to_decimal(credits)
        gl_jouhdr.debit =  to_decimal(debits)
        gl_jouhdr.remain =  to_decimal(remains)
        gl_jouhdr.batch = True

        if jour_type == 0:
            gl_jouhdr.batch = False
        pass
        t_jnr = gl_jouhdr.jnr

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters.counter
            gl_journal.fibukonto = g_list.fibukonto2
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit
            gl_journal.bemerk = g_list.bemerk

    post_it()

    return generate_output()