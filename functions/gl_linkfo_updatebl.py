#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Counters, Gl_journal, Htparam

g_list_data, G_list = create_model("G_list", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_linkfo_updatebl(pvilanguage:int, remains:Decimal, credits:[Decimal], debits:[Decimal], to_date:date, c_refno:string, c_bezeich:string, g_list_data:[G_list]):

    prepare_cache ([Gl_jouhdr, Counters, Gl_journal, Htparam])

    new_hdr:bool = True
    lvcarea:string = "gl-linkfo"
    gl_jouhdr = counters = gl_journal = htparam = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich


        nonlocal g_list

        return {}

    def create_header():

        nonlocal new_hdr, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich


        nonlocal g_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters.counter = counters.counter + 1
        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.datum = to_date
        gl_jouhdr.refno = c_refno
        gl_jouhdr.bezeich = c_bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1
        new_hdr = True


    def create_journals():

        nonlocal new_hdr, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, to_date, c_refno, c_bezeich


        nonlocal g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = gl_jouhdr.jnr
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1003)]})
        htparam.fdate = to_date
        pass

    create_header()
    create_journals()

    return generate_output()