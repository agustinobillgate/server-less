from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mathis, Mhis_line, Fa_op

def fa_upgrade_btn_gobl(g_list:[G_list], p_nr:int, nr:int, amt:decimal, user_init:str, qty:int, refno:str, datum:date, bezeich:str, debits:decimal, credits:decimal, remains:decimal):
    new_hdr:bool = True
    gl_jouhdr = counters = gl_journal = fa_artikel = mathis = mhis_line = fa_op = None

    g_list = fa_art = mhis = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

    Fa_art = Fa_artikel
    Mhis = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal fa_art, mhis


        nonlocal g_list, fa_art, mhis
        nonlocal g_list_list
        return {}

    def create_header():

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal fa_art, mhis


        nonlocal g_list, fa_art, mhis
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

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal fa_art, mhis


        nonlocal g_list, fa_art, mhis
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

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal fa_art, mhis


        nonlocal g_list, fa_art, mhis
        nonlocal g_list_list

        orig_bookval:decimal = 0
        qty:decimal = 0
        Fa_art = Fa_artikel
        Mhis = Mathis
        qty = fa_artikel.anzahl
        orig_bookval = fa_artikel.book_wert

        fa_artikel = db_session.query(Fa_artikel).first()
        fa_artikel.posted = True
        fa_artikel.warenwert = fa_artikel.warenwert + amt
        fa_artikel.book_wert = fa_artikel.book_wert + amt

        fa_artikel = db_session.query(Fa_artikel).first()

        mhis = db_session.query(Mhis).filter(
                (Mhis.nr == p_nr)).first()

        fa_art = db_session.query(Fa_art).filter(
                (Fa_art.nr == p_nr)).first()
        fa_art.loeschflag = 1
        fa_art.p_nr = nr
        fa_art.deleted = datum
        fa_art.did = user_init

        fa_art = db_session.query(Fa_art).first()
        mhis_line = Mhis_line()
        db_session.add(mhis_line)

        mhis_line.nr = nr
        mhis_line.datum = datum
        mhis_line.remark = "Upgrading Part: " + mhis.name +\
                "; Value  ==  " + trim(to_string(amt, ">,>>>,>>>,>>9.99"))

        mhis_line = db_session.query(Mhis_line).first()
        fa_op = Fa_op()
        db_session.add(fa_op)

        fa_op.nr = nr
        fa_op.opart = 4
        fa_op.datum = datum
        fa_op.zeit = get_current_time_in_seconds()
        fa_op.anzahl = qty
        fa_op.einzelpreis = orig_bookval
        fa_op.warenwert = amt
        fa_op.id = user_init
        fa_op.lscheinnr = refno
        fa_op.docu_nr = mhis.asset + " - " + mhis.name
        fa_op.lief_nr = fa_op.lief_nr

    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()