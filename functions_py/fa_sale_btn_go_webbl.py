#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------
"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning 
            - moved Counters(), Gl_jouhdr(), Gl_journal(), Mhis_line(), Fa_op() to global
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mhis_line, Fa_op
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model(
    "G_list", {
        "nr":int, 
        "jnr":int, 
        "fibukonto":string, 
        "debit":Decimal, 
        "credit":Decimal, 
        "bemerk":string, 
        "userinit":string, 
        "sysdate":date, 
        "zeit":int, 
        "chginit":string, 
        "chgdate":date, 
        "duplicate":bool,
        "acct_fibukonto":string, 
        "acct_bezeich":string
    }, {
        "sysdate": get_current_date(), 
        "chgdate": None, 
        "duplicate": True
    }
)

def fa_sale_btn_go_webbl(g_list_data:G_list, amt:Decimal, nr:int, datum:date, refno:string, bezeich:string, user_init:string, remains:Decimal, debits:Decimal, credits:Decimal, qty:int, fa_wert:Decimal, depn_wert:Decimal, book_wert:Decimal):

    prepare_cache ([Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mhis_line, Fa_op])

    sold_out = False
    output_list_data = []
    new_hdr:bool = True
    journal_nr:int = 0
    gl_acct = fa_artikel = None
    
    counters = Counters()
    gl_jouhdr = Gl_jouhdr()
    gl_journal = Gl_journal()
    mhis_line = Mhis_line()
    fa_op = Fa_op()
    
    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = output_list = None

    output_list_data, Output_list = create_model(
        "Output_list", {
            "succes_flag":bool, 
            "msg_str":string})

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal sold_out, output_list_data, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, output_list
        nonlocal output_list_data

        return {
            "sold_out": sold_out, 
            "output-list": output_list_data
        }

    def create_header():

        nonlocal sold_out, output_list_data, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, output_list
        nonlocal output_list_data

        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
        last_count, error_lock = get_output(next_counter_for_update(25))

        # if not counters:
        #     counters.counter_no = 25
        #     counters.counter_bez = "G/L Transaction Journal"
        #     counters.counter = 1
        #     journal_nr = int(str(counters.counter))

        #     db_session.add(counters)
            
        # elif counters:
        #     counters.counter = counters.counter + 1
        #     journal_nr = counters.counter
        
        journal_nr = last_count
        gl_jouhdr.jnr = journal_nr
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True

        db_session.add(gl_jouhdr)

    def create_journals():

        nonlocal sold_out, output_list_data, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, output_list
        nonlocal output_list_data

        for g_list in query(g_list_data):  # type: ignore G_list masih belum terisi
            gl_journal.jnr = journal_nr
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

            db_session.add(gl_journal)
            
        if remains == 0.01 or remains == -0.01:
            remains = Decimal(0)

        gl_jouhdr = get_cache (Gl_jouhdr, {
            "jnr": [(eq, journal_nr)]})

        if gl_jouhdr:
            gl_jouhdr.credit =  to_decimal(credits)
            gl_jouhdr.debit =  to_decimal(debits)
            gl_jouhdr.remain =  to_decimal(remains)
            
            pass

    def update_fix_asset():

        nonlocal sold_out, output_list_data, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, output_list
        nonlocal output_list_data

        orig_bookval = to_decimal("0.0")

        fa_artikel = get_cache (Fa_artikel, {
            "nr": [(eq, nr)]})

        if fa_artikel:
            qty = fa_artikel.anzah1
            sold_out = qty
            # sold_out = (fa_artikel.anzahl == qty)
            orig_bookval =  to_decimal(fa_artikel.book_wert)
            fa_artikel.posted = True

            if sold_out:
                fa_artikel.loeschflag = 1
                fa_artikel.deleted = get_current_date()
            else:
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.warenwert =  to_decimal(fa_artikel.warenwert - fa_wert)  
                fa_artikel.depn_wert =  to_decimal(fa_artikel.depn_wert -depn_wert) 
                fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert - book_wert) 
            
            fa_artikel.did = user_init
            
            mhis_line.nr = nr
            mhis_line.datum = datum
            mhis_line.remark = "Sold Out: qty = " + str(qty) + "; Amount = " + trim(to_string(amt, ">>>,>>>,>>>,>>9.99"))
            
            db_session.add(mhis_line)

            fa_op.nr = nr
            fa_op.opart = 3
            fa_op.datum = datum
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis =  to_decimal(orig_bookval)
            fa_op.warenwert =  to_decimal(book_wert)
            fa_op.id = user_init
            fa_op.lscheinnr = refno
            fa_op.docu_nr = bezeich
            fa_op.lief_nr = fa_artikel.lief_nr
            
            db_session.add(fa_op)
            
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.succes_flag = True 
            output_list.msg_str = "Transfer to GL completed successfully."

            return

    if remains == 0.01 or remains == -0.01:
        remains =  Decimal(0)

    if remains != 0:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.succes_flag = False
        output_list.msg_str = "Transaction cannot be transferred because GL is not balanced."

        return generate_output()
    
    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()