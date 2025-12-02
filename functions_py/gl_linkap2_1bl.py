#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Counters, Gl_journal, Htparam
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model("G_list", {"nr":int, "remark":string, "docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_linkap2_1bl(pvilanguage:int, remains:Decimal, credits:Decimal, debits:Decimal, to_date:date, c_refno:string, c_bezeich:string, g_list_data:[G_list]):

    prepare_cache ([Gl_jouhdr, Counters, Gl_journal, Htparam])

    msg_str = ""
    new_hdr:bool = True
    hdr_found:bool = False
    lvcarea:string = "gl-linkap2_1"
    gl_jouhdr = counters = gl_journal = htparam = None

    g_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    c_bezeich = c_bezeich.strip()
    c_refno = c_refno.strip()


    def generate_output():
        nonlocal msg_str, new_hdr, hdr_found, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, credits, debits, to_date, c_refno, c_bezeich


        nonlocal g_list

        return {"msg_str": msg_str}

    def verify_refno():

        nonlocal msg_str, new_hdr, hdr_found, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, credits, debits, to_date, c_refno, c_bezeich


        nonlocal g_list


        msg_str = ""

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(Gl_jouhdr.refno == c_refno).first()

        if gl_jouhdr:
            msg_str = "Refno " + c_refno + " Already Exists: " + to_string(gl_jouhdr.datum) + " " + gl_jouhdr.bezeich
            hdr_found = True


    def create_header():

        nonlocal msg_str, new_hdr, hdr_found, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, credits, debits, to_date, c_refno, c_bezeich


        nonlocal g_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
        counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 25)).with_for_update().first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters.counter = counters.counter + 1
        gl_jouhdr.jnr = counters.counter  

        gl_jouhdr.refno = c_refno
        gl_jouhdr.datum = to_date
        gl_jouhdr.bezeich = c_bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 4
        new_hdr = True


    def create_journals():

        nonlocal msg_str, new_hdr, hdr_found, lvcarea, gl_jouhdr, counters, gl_journal, htparam
        nonlocal pvilanguage, remains, credits, debits, to_date, c_refno, c_bezeich


        nonlocal g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            # gl_journal.jnr = counters.counter
            gl_journal.jnr = last_count


            
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains =  to_decimal("0")
        
        db_session.refresh(gl_jouhdr, with_for_update=True)

        gl_jouhdr.credit =  to_decimal(credits)
        gl_jouhdr.debit =  to_decimal(debits)
        gl_jouhdr.remain =  to_decimal(remains)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 1118)]})
        htparam.fdate = to_date
   

    verify_refno()

    if hdr_found :
        return generate_output()
    
    create_header()
    create_journals()

    return generate_output()