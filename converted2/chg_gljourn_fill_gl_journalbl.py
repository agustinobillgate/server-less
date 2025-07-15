#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.update_bemerkbl import update_bemerkbl
from datetime import date
from models import Gl_jouhdr, Gl_journal, Gl_acct, Bediener, Res_history, Queasy

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def chg_gljourn_fill_gl_journalbl(case_type:int, jnr:int, comment:string, user_init:string, jou_recid:int, b1_recid:int, t_bezeich:string, t_refno:string, g_list_data:[G_list]):

    prepare_cache ([Gl_jouhdr, Gl_journal, Gl_acct, Bediener, Res_history, Queasy])

    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    b1_list_data = []
    fibukonto:string = ""
    bemerk:string = ""
    debit:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    datum:date = None
    gl_jouhdr = gl_journal = gl_acct = bediener = res_history = queasy = None

    b1_list = g_list = None

    b1_list_data, B1_list = create_model("B1_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "bezeich":string, "chginit":string, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":string, "tax_amount":string, "tot_amt":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, b1_list_data, fibukonto, bemerk, debit, credit, datum, gl_jouhdr, gl_journal, gl_acct, bediener, res_history, queasy
        nonlocal case_type, jnr, comment, user_init, jou_recid, b1_recid, t_bezeich, t_refno


        nonlocal b1_list, g_list
        nonlocal b1_list_data

        return {"debits": debits, "credits": credits, "remains": remains, "b1-list": b1_list_data}

    def update_queasy_345(jnr:int, datum:date, bezeich:string):

        nonlocal debits, credits, remains, b1_list_data, fibukonto, bemerk, debit, credit, gl_jouhdr, gl_journal, gl_acct, bediener, res_history, queasy
        nonlocal case_type, comment, user_init, jou_recid, b1_recid, t_bezeich, t_refno


        nonlocal b1_list, g_list
        nonlocal b1_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 345)],"number1": [(eq, jnr)],"date1": [(eq, datum)]})

        if queasy:
            pass
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 345
            queasy.number1 = jnr
            queasy.number2 = get_current_time_in_seconds()
            queasy.char1 = bezeich
            queasy.date1 = datum
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass

    if case_type == 1:

        g_list = query(g_list_data, first=True)

        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = jnr
        gl_journal.fibukonto = g_list.fibukonto
        gl_journal.bemerk = comment
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        fibukonto = g_list.fibukonto
        bemerk = comment
        debit =  to_decimal(g_list.debit)
        credit =  to_decimal(g_list.credit)
        datum = gl_jouhdr.datum


        gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(g_list.debit)
        gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(g_list.credit)
        gl_jouhdr.remain =  to_decimal(gl_jouhdr.remain) + to_decimal(g_list.debit) - to_decimal(g_list.credit)
        gl_jouhdr.bezeich = t_bezeich
        gl_jouhdr.refno = t_refno
        gl_journal.debit =  to_decimal(g_list.debit)
        gl_journal.credit =  to_decimal(g_list.credit)
        pass
        pass

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.fibukonto = g_list.fibukonto
        b1_list.debit =  to_decimal(g_list.debit)
        b1_list.credit =  to_decimal(g_list.credit)
        b1_list.bemerk = comment
        b1_list.bezeich = gl_acct.bezeich
        b1_list.chginit = user_init
        b1_list.chgdate = get_current_date()
        b1_list.activeflag = gl_journal.activeflag
        b1_list.rec_gl_journ = gl_journal._recid

        if num_entries(gl_acct.bemerk, ";") > 1:
            b1_list.tax_code = entry(1, gl_acct.bemerk, ";")

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Add Journal, Date: " + to_string(datum) + ", AcctNo: " + to_string(fibukonto) + ", Remark: " + to_string(comment) + ", debit: " + to_string(debit) + ", credit: " + to_string(credit)
            res_history.action = "G/L"


            pass
            pass
        update_queasy_345(jnr, datum, gl_jouhdr.bezeich)

    elif case_type == 2:

        g_list = query(g_list_data, first=True)

        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})

        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, jou_recid)]})
        fibukonto = gl_journal.fibukonto
        bemerk = gl_journal.bemerk
        debit =  to_decimal(gl_journal.debit)
        credit =  to_decimal(gl_journal.credit)
        datum = gl_jouhdr.datum


        gl_journal.chginit = user_init
        gl_journal.chgdate = get_current_date()
        gl_journal.bemerk = comment
        gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(g_list.debit) - to_decimal(gl_journal.debit)
        gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(g_list.credit) - to_decimal(gl_journal.credit)
        gl_jouhdr.remain =  to_decimal(gl_jouhdr.remain) + to_decimal(g_list.debit) - to_decimal(g_list.credit) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
        gl_jouhdr.bezeich = t_bezeich
        gl_jouhdr.refno = t_refno
        gl_journal.fibukonto = g_list.fibukonto
        gl_journal.debit =  to_decimal(g_list.debit)
        gl_journal.credit =  to_decimal(g_list.credit)
        pass
        pass
        get_output(update_bemerkbl(jou_recid))

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.fibukonto = g_list.fibukonto
        b1_list.debit =  to_decimal(g_list.debit)
        b1_list.credit =  to_decimal(g_list.credit)
        b1_list.bemerk = comment
        b1_list.chginit = user_init
        b1_list.chgdate = get_current_date()
        b1_list.activeflag = gl_journal.activeflag
        b1_list.rec_gl_journ = b1_recid
        b1_list.bezeich = gl_acct.bezeich

        if num_entries(gl_acct.bemerk, ";") > 1:
            b1_list.tax_code = entry(1, gl_acct.bemerk, ";")

        if gl_journal.fibukonto.lower()  != (fibukonto).lower() :

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", AcctNo From: " + fibukonto + " To: " + gl_journal.fibukonto
                res_history.action = "G/L"


                pass
                pass

        if gl_journal.bemerk.lower()  != (bemerk).lower() :

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", Notes From: " + bemerk + " To: " + gl_journal.bemerk
                res_history.action = "G/L"


                pass
                pass

        if gl_journal.debit != debit:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", debit From: " + to_string(debit) + " To: " + to_string(gl_journal.debit)
                res_history.action = "G/L"


                pass
                pass

        if gl_journal.credit != credit:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", credit From: " + to_string(credit) + " To: " + to_string(gl_journal.credit)
                res_history.action = "G/L"


                pass
                pass
        update_queasy_345(jnr, datum, gl_jouhdr.bezeich)
    debits =  to_decimal(gl_jouhdr.debit)
    credits =  to_decimal(gl_jouhdr.credit)
    remains =  to_decimal(gl_jouhdr.remain)

    return generate_output()