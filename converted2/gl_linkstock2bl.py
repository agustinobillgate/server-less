#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Counters, Queasy, Gl_journal

g_list_data, G_list = create_model("G_list", {"docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "add_note":string, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_linkstock2bl(pvilanguage:int, link_in:bool, to_date:date, remains:Decimal, credits:Decimal, debits:Decimal, refno:string, datum:date, bezeich:string, jtype:int, g_list_data:[G_list]):

    prepare_cache ([Htparam, Gl_jouhdr, Counters, Queasy, Gl_journal])

    new_hdr:bool = True
    lvcarea:string = "gl-linkstock"
    htparam = gl_jouhdr = counters = queasy = gl_journal = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, link_in, to_date, remains, credits, debits, refno, datum, bezeich, jtype


        nonlocal g_list

        return {}

    def create_header():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, link_in, to_date, remains, credits, debits, refno, datum, bezeich, jtype


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
        pass
        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = jtype
        new_hdr = True

        if not link_in:

            queasy = get_cache (Queasy, {"key": [(eq, 333)],"char1": [(eq, refno)],"char3": [(eq, "outgoing jurnal")]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 333
                queasy.char1 = refno
                queasy.char2 = bezeich
                queasy.char3 = "Outgoing Jurnal"
                queasy.date1 = datum
                queasy.number1 = jtype


    def create_journals():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, link_in, to_date, remains, credits, debits, refno, datum, bezeich, jtype


        nonlocal g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters.counter
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk + g_list.add_note
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

    create_header()
    create_journals()

    if link_in:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1035)]})

    if htparam.fdate < to_date:
        htparam.fdate = to_date
    pass

    return generate_output()