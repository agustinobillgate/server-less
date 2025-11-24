#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 18/7/25
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.update_bemerkbl import update_bemerkbl
from models import Gl_jouhdr, Gl_journal, Gl_acct

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "bemerk":string, "jou_recid":int, "b1_recid":int, "flag":int}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def chg_gljourn_fill_gl_journal_vhpwebbl(jnr:int, user_init:string, t_bezeich:string, t_refno:string, g_list_data:[G_list]):

    prepare_cache ([Gl_jouhdr, Gl_acct])

    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    b1_list_data = []
    debitval:Decimal = to_decimal("0.0")
    creditval:Decimal = to_decimal("0.0")
    tmp_activeflag:int = 0
    gl_jouhdr = gl_journal = gl_acct = None

    b1_list = g_list = buffglhdr = None

    b1_list_data, B1_list = create_model("B1_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "bezeich":string, "chginit":string, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":string, "tax_amount":string, "tot_amt":string})

    Buffglhdr = create_buffer("Buffglhdr",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, b1_list_data, debitval, creditval, tmp_activeflag, gl_jouhdr, gl_journal, gl_acct
        nonlocal jnr, user_init, t_bezeich, t_refno
        nonlocal buffglhdr


        nonlocal b1_list, g_list, buffglhdr
        nonlocal b1_list_data

        return {"debits": debits, "credits": credits, "remains": remains, "b1-list": b1_list_data}


    for g_list in query(g_list_data):

        if g_list.flag == 1:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.jnr == jnr)).order_by(Gl_jouhdr._recid).all():

                # Rd, 24/11/2025, get gl_jouhdr dengan for update
                # buffglhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, gl_jouhdr._recid)]})
                buffglhdr = db_session.query(Gl_jouhdr).filter(
                             (Gl_jouhdr._recid == gl_jouhdr._recid)).with_for_update().first()

                if buffglhdr:
                    pass
                    gl_journal = Gl_journal()
                    db_session.add(gl_journal)

                    gl_journal.jnr = jnr


                    gl_journal.fibukonto = g_list.fibukonto
                    gl_journal.bemerk = g_list.bemerk
                    gl_journal.userinit = user_init
                    gl_journal.zeit = get_current_time_in_seconds()
                    buffglhdr.debit =  to_decimal(buffglhdr.debit) + to_decimal(g_list.debit)
                    buffglhdr.credit =  to_decimal(buffglhdr.credit) + to_decimal(g_list.credit)
                    buffglhdr.remain =  to_decimal(buffglhdr.remain) + to_decimal(g_list.debit) - to_decimal(g_list.credit)
                    debitval =  to_decimal(debitval) + to_decimal(g_list.debit)
                    creditval =  to_decimal(creditval) + to_decimal(g_list.credit)
                    buffglhdr.bezeich = t_bezeich
                    buffglhdr.refno = t_refno
                    gl_journal.debit =  to_decimal(g_list.debit)
                    gl_journal.credit =  to_decimal(g_list.credit)
                    pass

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})
                    b1_list = B1_list()
                    b1_list_data.append(b1_list)

                    b1_list.fibukonto = g_list.fibukonto
                    b1_list.debit =  to_decimal(g_list.debit)
                    b1_list.credit =  to_decimal(g_list.credit)
                    b1_list.bemerk = g_list.bemerk
                    b1_list.bezeich = gl_acct.bezeich
                    b1_list.chginit = user_init
                    b1_list.chgdate = get_current_date()
                    b1_list.activeflag = gl_journal.activeflag
                    b1_list.rec_gl_journ = gl_journal._recid

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        b1_list.tax_code = entry(1, gl_acct.bemerk, ";")


                    pass
                    pass
                debits =  to_decimal(debits) + to_decimal(gl_jouhdr.debit)
                credits =  to_decimal(credits) + to_decimal(gl_jouhdr.credit)
                remains =  to_decimal(remains) + to_decimal(gl_jouhdr.remain)

        elif g_list.flag == 2:
            # Rd, 24/11/2025, get gl_jouhdr dengan for update
            # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.jnr == jnr)).with_for_update().first()

            if gl_jouhdr:
                # Rd, 24/11/2025, get gl_journal dengan for update
                # gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.jou_recid)]})
                gl_journal = db_session.query(Gl_journal).filter(
                             (Gl_journal._recid == g_list.jou_recid)).with_for_update().first()

                if gl_journal:
                    pass
                    pass
                    gl_journal.chginit = user_init
                    gl_journal.chgdate = get_current_date()
                    gl_journal.bemerk = g_list.bemerk
                    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(g_list.debit) - to_decimal(gl_journal.debit)
                    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(g_list.credit) - to_decimal(gl_journal.credit)
                    gl_jouhdr.remain =  to_decimal(gl_jouhdr.remain) + to_decimal(g_list.debit) - to_decimal(g_list.credit) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                    gl_jouhdr.bezeich = t_bezeich
                    gl_jouhdr.refno = t_refno
                    gl_journal.fibukonto = g_list.fibukonto
                    gl_journal.debit =  to_decimal(g_list.debit)
                    gl_journal.credit =  to_decimal(g_list.credit)
                    debitval =  to_decimal(debitval) + to_decimal(g_list.debit)
                    creditval =  to_decimal(creditval) + to_decimal(g_list.credit)
                    tmp_activeflag = gl_journal.activeflag
                    pass
                    pass
                    pass
                else:
                    tmp_activeflag = 0
                debits =  to_decimal(gl_jouhdr.debit)
                credits =  to_decimal(gl_jouhdr.credit)
                remains =  to_decimal(gl_jouhdr.remain)
                pass
            get_output(update_bemerkbl(g_list.jou_recid))

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

            if gl_acct:
                b1_list = B1_list()
                b1_list_data.append(b1_list)

                b1_list.fibukonto = g_list.fibukonto
                b1_list.debit =  to_decimal(g_list.debit)
                b1_list.credit =  to_decimal(g_list.credit)
                b1_list.bemerk = g_list.bemerk
                b1_list.chginit = user_init
                b1_list.chgdate = get_current_date()
                b1_list.activeflag = tmp_activeflag
                b1_list.rec_gl_journ = g_list.b1_recid
                b1_list.bezeich = gl_acct.bezeich

                if num_entries(gl_acct.bemerk, ";") > 1:
                    b1_list.tax_code = entry(1, gl_acct.bemerk, ";")

        elif g_list.flag == 3:
            # Rd, 24/11/2025, get gl_journal dengan for update
            # gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.b1_recid)]})
            gl_journal = db_session.query(Gl_journal).filter(
                         (Gl_journal._recid == g_list.b1_recid)).with_for_update().first()

            if gl_journal:
                # Rd, 24/11/2025, get gl_jouhdr dengan for update
                # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
                gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                             (Gl_jouhdr.jnr == jnr)).with_for_update().first()

                if gl_jouhdr:
                    pass
                    pass
                    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_journal.debit)
                    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) - to_decimal(gl_journal.credit)
                    gl_jouhdr.remain =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_jouhdr.credit)
                    credits =  to_decimal(gl_jouhdr.credit)
                    remains =  to_decimal(gl_jouhdr.remain)
                    db_session.delete(gl_journal)
                    pass
                    debits =  to_decimal(gl_jouhdr.debit)
                    credits =  to_decimal(gl_jouhdr.credit)
                    remains =  to_decimal(gl_jouhdr.remain)
                    pass
                    pass

    return generate_output()