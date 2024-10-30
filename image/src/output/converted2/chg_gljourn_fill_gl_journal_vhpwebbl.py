from functions.additional_functions import *
import decimal
from functions.update_bemerkbl import update_bemerkbl
from models import Gl_jouhdr, Gl_journal, Gl_acct

g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "bemerk":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def chg_gljourn_fill_gl_journal_vhpwebbl(case_type:int, jnr:int, user_init:str, jou_recid:int, b1_recid:int, t_bezeich:str, t_refno:str, g_list_list:[G_list]):
    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    b1_list_list = []
    gl_jouhdr = gl_journal = gl_acct = None

    b1_list = g_list = None

    b1_list_list, B1_list = create_model("B1_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "bezeich":str, "chginit":str, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":str, "tax_amount":str, "tot_amt":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, b1_list_list, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, jnr, user_init, jou_recid, b1_recid, t_bezeich, t_refno


        nonlocal b1_list, g_list
        nonlocal b1_list_list

        return {"debits": debits, "credits": credits, "remains": remains, "b1-list": b1_list_list}


    if case_type == 1:

        g_list = query(g_list_list, first=True)

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.jnr == jnr)).first()
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = jnr
        gl_journal.fibukonto = g_list.fibukonto
        gl_journal.bemerk = g_list.bemerk
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(g_list.debit)
        gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(g_list.credit)
        gl_jouhdr.remain =  to_decimal(gl_jouhdr.remain) + to_decimal(g_list.debit) - to_decimal(g_list.credit)
        gl_jouhdr.bezeich = t_bezeich
        gl_jouhdr.refno = t_refno
        gl_journal.debit =  to_decimal(g_list.debit)
        gl_journal.credit =  to_decimal(g_list.credit)

        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == g_list.fibukonto)).first()
        b1_list = B1_list()
        b1_list_list.append(b1_list)

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

    elif case_type == 2:

        g_list = query(g_list_list, first=True)

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.jnr == jnr)).first()

        gl_journal = db_session.query(Gl_journal).filter(
                 (Gl_journal._recid == jou_recid)).first()
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
        get_output(update_bemerkbl(jou_recid))

        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == g_list.fibukonto)).first()
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.fibukonto = g_list.fibukonto
        b1_list.debit =  to_decimal(g_list.debit)
        b1_list.credit =  to_decimal(g_list.credit)
        b1_list.bemerk = g_list.bemerk
        b1_list.chginit = user_init
        b1_list.chgdate = get_current_date()
        b1_list.activeflag = gl_journal.activeflag
        b1_list.rec_gl_journ = b1_recid
        b1_list.bezeich = gl_acct.bezeich

        if num_entries(gl_acct.bemerk, ";") > 1:
            b1_list.tax_code = entry(1, gl_acct.bemerk, ";")


    debits =  to_decimal(gl_jouhdr.debit)
    credits =  to_decimal(gl_jouhdr.credit)
    remains =  to_decimal(gl_jouhdr.remain)

    return generate_output()