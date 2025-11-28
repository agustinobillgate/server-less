#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mhis_line, Fa_op
from functions.next_counter_for_update import next_counter_for_update
g_list_data, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "acct_bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def fa_sale_btn_gobl(g_list_data:[G_list], amt:Decimal, nr:int, datum:date, refno:string, bezeich:string, 
                     user_init:string, remains:Decimal, debits:Decimal, credits:Decimal, qty:int, fa_wert:Decimal, depn_wert:Decimal, book_wert:Decimal):

    prepare_cache ([Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mhis_line, Fa_op])

    sold_out = False
    new_hdr:bool = True
    journal_nr:int = 0
    gl_acct = gl_jouhdr = counters = gl_journal = fa_artikel = mhis_line = fa_op = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = None

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    refno = refno.strip()
    bezeich = bezeich.strip()
    user_init = user_init.strip()


    def generate_output():
        nonlocal sold_out, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        return {"sold_out": sold_out}

    def create_header():

        nonlocal sold_out, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
            # counters.counter = 1
            # journal_nr = counters.counter

        # elif counters:
            # pass
            # counters.counter = counters.counter + 1
            # journal_nr = counters.counter

        last_count, error_lock = get_output(next_counter_for_update(25))
        journal_nr = last_count


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = journal_nr
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True


    def create_journals():

        nonlocal sold_out, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = journal_nr
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains =  to_decimal("0")

        # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, journal_nr)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.jnr == journal_nr)).with_for_update().first()

        if gl_jouhdr:
            # pass
            gl_jouhdr.credit =  to_decimal(credits)
            gl_jouhdr.debit =  to_decimal(debits)
            gl_jouhdr.remain =  to_decimal(remains)
            # pass
            # pass
            db_session.refresh(gl_jouhdr,with_for_update=True)


    def update_fix_asset():

        nonlocal sold_out, new_hdr, journal_nr, gl_acct, gl_jouhdr, counters, gl_journal, fa_artikel, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        orig_bookval:Decimal = to_decimal("0.0")

        # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, nr)]})
        fa_artikel = db_session.query(Fa_artikel).filter(
                 (Fa_artikel.nr == nr)).with_for_update().first()

        if fa_artikel:
            sold_out = (fa_artikel.anzahl == qty)
            orig_bookval =  to_decimal(fa_artikel.book_wert)
            pass
            fa_artikel.posted = True

            if sold_out:
                fa_artikel.loeschflag = 1
                fa_artikel.deleted = get_current_date()
            else:
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.warenwert =  to_decimal(fa_artikel.warenwert) - to_decimal(fa_wert)
                fa_artikel.depn_wert =  to_decimal(fa_artikel.depn_wert) - to_decimal(depn_wert)
                fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert) - to_decimal(book_wert)
            fa_artikel.did = user_init
            # pass
            db_session.refresh(fa_artikel,with_for_update=True)
            mhis_line = Mhis_line()
            db_session.add(mhis_line)

            mhis_line.nr = nr
            mhis_line.datum = datum
            mhis_line.remark = "Sold Out: qty = " + to_string(qty) + "; Amount = " + trim(to_string(amt, ">>>,>>>,>>>,>>9.99"))
            pass
            fa_op = Fa_op()
            db_session.add(fa_op)

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
            pass

    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()