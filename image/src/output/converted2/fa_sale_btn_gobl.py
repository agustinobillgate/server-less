#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Fa_artikel, Counters, Gl_journal, Mhis_line, Fa_op

g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "acct_bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def fa_sale_btn_gobl(g_list_list:[G_list], amt:Decimal, nr:int, datum:date, refno:string, bezeich:string, user_init:string, remains:Decimal, debits:Decimal, credits:Decimal, qty:int, fa_wert:Decimal, depn_wert:Decimal, book_wert:Decimal):

    prepare_cache ([Gl_jouhdr, Fa_artikel, Counters, Gl_journal, Mhis_line, Fa_op])

    sold_out = False
    new_hdr:bool = True
    gl_acct = gl_jouhdr = fa_artikel = counters = gl_journal = mhis_line = fa_op = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = None

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        return {"sold_out": sold_out}

    def create_header():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
        counters.counter = counters.counter + 1
        pass
        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True


    def create_journals():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        for g_list in query(g_list_list):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters.counter
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


    def update_fix_asset():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal amt, nr, datum, refno, bezeich, user_init, remains, debits, credits, qty, fa_wert, depn_wert, book_wert
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        orig_bookval:Decimal = to_decimal("0.0")
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
        pass
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


    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, nr)]})
    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()