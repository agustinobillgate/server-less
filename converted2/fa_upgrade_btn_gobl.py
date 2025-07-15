#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mathis, Mhis_line, Fa_op

g_list_data, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def fa_upgrade_btn_gobl(g_list_data:[G_list], p_nr:int, nr:int, amt:Decimal, user_init:string, qty:int, refno:string, datum:date, bezeich:string, debits:Decimal, credits:Decimal, remains:Decimal):

    prepare_cache ([Gl_jouhdr, Counters, Gl_journal, Fa_artikel, Mathis, Mhis_line, Fa_op])

    new_hdr:bool = True
    gl_jouhdr = counters = gl_journal = fa_artikel = mathis = mhis_line = fa_op = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal p_nr, nr, amt, user_init, qty, refno, datum, bezeich, debits, credits, remains


        nonlocal g_list

        return {}

    def create_header():

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal p_nr, nr, amt, user_init, qty, refno, datum, bezeich, debits, credits, remains


        nonlocal g_list


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

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal p_nr, nr, amt, user_init, qty, refno, datum, bezeich, debits, credits, remains


        nonlocal g_list

        for g_list in query(g_list_data):
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

        nonlocal new_hdr, gl_jouhdr, counters, gl_journal, fa_artikel, mathis, mhis_line, fa_op
        nonlocal p_nr, nr, amt, user_init, refno, datum, bezeich, debits, credits, remains


        nonlocal g_list

        orig_bookval:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        fa_art = None
        mhis = None
        Fa_art =  create_buffer("Fa_art",Fa_artikel)
        Mhis =  create_buffer("Mhis",Mathis)

        fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, p_nr)]})

        if fa_artikel:
            qty =  to_decimal(fa_artikel.anzahl)
            orig_bookval =  to_decimal(fa_artikel.book_wert)


            pass
            fa_artikel.posted = True
            fa_artikel.warenwert =  to_decimal(fa_artikel.warenwert) + to_decimal(amt)
            fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert) + to_decimal(amt)


            pass

            mhis = get_cache (Mathis, {"nr": [(eq, p_nr)]})

            fa_art = get_cache (Fa_artikel, {"nr": [(eq, p_nr)]})
            fa_art.loeschflag = 1
            fa_art.p_nr = nr
            fa_art.deleted = datum
            fa_art.did = user_init


            pass
            mhis_line = Mhis_line()
            db_session.add(mhis_line)

            mhis_line.nr = nr
            mhis_line.datum = datum
            mhis_line.remark = "Upgrading Part: " + mhis.name +\
                    "; Value = " + trim(to_string(amt, ">,>>>,>>>,>>9.99"))


            pass
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = nr
            fa_op.opart = 4
            fa_op.datum = datum
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis =  to_decimal(orig_bookval)
            fa_op.warenwert =  to_decimal(amt)
            fa_op.id = user_init
            fa_op.lscheinnr = refno
            fa_op.docu_nr = mhis.asset + " - " + mhis.name
            fa_op.lief_nr = fa_op.lief_nr


            pass

    create_header()
    create_journals()
    update_fix_asset()

    return generate_output()