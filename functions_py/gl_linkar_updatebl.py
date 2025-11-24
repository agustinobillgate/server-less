#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Counters, Gl_jouhdr, Gl_journal, Htparam
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model("G_list", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_linkar_updatebl(pvilanguage:int, remains:Decimal, credits:[Decimal], debits:[Decimal], to_date:date, 
                       c_refno:string, c_bezeich:string, datum:date, g_list_data:[G_list]):

    prepare_cache ([Counters, Gl_jouhdr, Gl_journal, Htparam])

    new_hdr:bool = True
    curr_counter:int = 0
    lvcarea:string = "gl-linkar"
    counters = gl_jouhdr = gl_journal = htparam = None

    g_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    c_bezeich = c_bezeich.strip()
    c_refno = c_refno.strip()

    def generate_output():
        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich, datum


        nonlocal g_list

        return {}

    def create_header():

        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich, datum


        nonlocal g_list

        counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)
            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        # counters.counter = counters.counter + 1

        last_count, error_lock = next_counter_for_update(25)

        # curr_counter = counters.counter
        curr_counter = last_count


        pass
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = curr_counter
        gl_jouhdr.refno = c_refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = c_bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 2
        new_hdr = True


        pass


    def create_journals():

        nonlocal new_hdr, curr_counter, lvcarea, counters, gl_jouhdr, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich, datum


        nonlocal g_list

        for g_list in query(g_list_data, filters=(lambda g_list:(round(g_list.debit, 2) != 0 or round(g_list.credit, 2) != 0))):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = curr_counter
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk + g_list.add_info
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains =  to_decimal("0")
        pass
        gl_jouhdr.credit =  to_decimal(credits)
        gl_jouhdr.debit =  to_decimal(debits)
        gl_jouhdr.remain =  to_decimal(remains)


        pass
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})
        htparam.fdate = datum


        pass

    create_header()
    create_journals()

    return generate_output()