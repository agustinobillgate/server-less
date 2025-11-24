#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Counters, Queasy, Gl_journal
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model("G_list", {"docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "add_note":string, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_linkcompli2bl(pvilanguage:int, remains:Decimal, credits:Decimal, debits:Decimal, to_date:date, refno:string, 
                     datum:date, bezeich:string, g_list_data:[G_list]):

    prepare_cache ([Htparam, Gl_jouhdr, Counters, Queasy, Gl_journal])

    new_hdr:bool = True
    lvcarea:string = "gl-linkcompli"
    htparam = gl_jouhdr = counters = queasy = gl_journal = None

    g_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    refno = refno.strip()
    bezeich = bezeich.strip()
    docu_nr = docu_nr.strip()


    def generate_output():
        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, remains, credits, debits, to_date, refno, datum, bezeich


        nonlocal g_list

        return {}

    def create_header():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, remains, credits, debits, to_date, refno, datum, bezeich, last_count


        nonlocal g_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")

        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(25))
        pass
        # gl_jouhdr.jnr = counters.counter
        gl_jouhdr.jnr = last_count

        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 3
        new_hdr = True

        queasy = get_cache (Queasy, {"key": [(eq, 333)],"char1": [(eq, refno)],"char3": [(eq, "compliment journal")]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 333
            queasy.char1 = refno
            queasy.char2 = bezeich
            queasy.char3 = "Compliment Journal"
            queasy.date1 = datum
            queasy.number1 = gl_jouhdr.jtype


    def create_journals():

        nonlocal new_hdr, lvcarea, htparam, gl_jouhdr, counters, queasy, gl_journal
        nonlocal pvilanguage, remains, credits, debits, to_date, refno, datum, bezeich, last_count


        nonlocal g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            # gl_journal.jnr = counters.counter
            gl_journal.jnr = last_count

            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit = to_decimal(round(g_list.debit , 2))
            gl_journal.credit = to_decimal(round(g_list.credit , 2))
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1123)]})
    htparam.fdate = to_date
    pass

    return generate_output()