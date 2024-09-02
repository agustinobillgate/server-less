from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Fa_artikel, Counters, Gl_journal, Mhis_line, Fa_op

def fa_sale_btn_gobl(g_list:[G_list], amt:decimal, nr:int, datum:date, refno:str, bezeich:str, user_init:str, remains:decimal, debits:decimal, credits:decimal, qty:int, fa_wert:decimal, depn_wert:decimal, book_wert:decimal):
    sold_out = False
    new_hdr:bool = True
    gl_acct = gl_jouhdr = fa_artikel = counters = gl_journal = mhis_line = fa_op = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "acct_fibukonto":str, "acct_bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct
    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list
        return {"sold_out": sold_out}

    def create_header():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
        counters.counter = counters.counter + 1

        counters = db_session.query(Counters).first()
        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True

    def create_journals():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list

        for g_list in query(g_list_list):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters.counter
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit = g_list.debit
            gl_journal.credit = g_list.credit
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains = 0

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        gl_jouhdr.credit = credits
        gl_jouhdr.debit = debits
        gl_jouhdr.remain = remains

        gl_jouhdr = db_session.query(Gl_jouhdr).first()

    def update_fix_asset():

        nonlocal sold_out, new_hdr, gl_acct, gl_jouhdr, fa_artikel, counters, gl_journal, mhis_line, fa_op
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list

        orig_bookval:decimal = 0
        sold_out = (fa_artikel.anzahl == qty)
        orig_bookval = fa_artikel.book_wert

        fa_artikel = db_session.query(Fa_artikel).first()
        fa_artikel.posted = True

        if sold_out:
            fa_artikel.loeschflag = 1
            fa_artikel.deleted = get_current_date()
        else:
            fa_artikel.anzahl = fa_artikel.anzahl - qty
            fa_artikel.warenwert = fa_artikel.warenwert - fa_wert
            fa_artikel.depn_wert = fa_artikel.depn_wert - depn_wert
            fa_artikel.book_wert = fa_artikel.book_wert - book_wert
        fa_artikel.did = user_init

        fa_artikel = db_session.query(Fa_artikel).first()
        mhis_line = Mhis_line()
        db_session.add(mhis_line)

        mhis_line.nr = nr
        mhis_line.datum = datum
        mhis_line.remark = "Sold Out: qty  ==  " + to_string(qty) + "; Amount  ==  " + trim(to_string(amt, ">>>,>>>,>>>,>>9.99"))

        mhis_line = db_session.query(Mhis_line).first()
        fa_op = Fa_op()
        db_session.add(fa_op)

        fa_op.nr = nr
        fa_op.opart = 3
        fa_op.datum = datum
        fa_op.zeit = get_current_time_in_seconds()
        fa_op.anzahl = qty
        fa_op.einzelpreis = orig_bookval
        fa_op.warenwert = book_wert
        fa_op.id = user_init
        fa_op.lscheinnr = refno
        fa_op.docu_nr = bezeich
        fa_op.lief_nr = fa_artikel.lief_nr


    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == nr)).first()
    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()