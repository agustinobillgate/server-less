from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_acct, Gl_jouhdr, Gl_journal, Gl_accthis, Bediener, Res_history

def close_adjustmentbl(pvilanguage:int, user_init:str):
    closed = False
    msg_str = ""
    lvcarea:str = "close-adjustment"
    curr_date:date = None
    curr_month:int = 0
    curr_year:int = 0
    prev_month:int = 0
    from_month:int = 0
    to_month:int = 0
    pnl_acct:str = ""
    balance:decimal = to_decimal("0.0")
    profit:decimal = to_decimal("0.0")
    lost:decimal = to_decimal("0.0")
    i:int = 0
    htparam = gl_acct = gl_jouhdr = gl_journal = gl_accthis = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal closed, msg_str, lvcarea, curr_date, curr_month, curr_year, prev_month, from_month, to_month, pnl_acct, balance, profit, lost, i, htparam, gl_acct, gl_jouhdr, gl_journal, gl_accthis, bediener, res_history
        nonlocal pvilanguage, user_init

        return {"closed": closed, "msg_str": msg_str}

    def process_journal(inp_jnr:int):

        nonlocal closed, msg_str, lvcarea, curr_date, curr_month, curr_year, prev_month, from_month, to_month, pnl_acct, balance, profit, lost, htparam, gl_acct, gl_jouhdr, gl_journal, gl_accthis, bediener, res_history
        nonlocal pvilanguage, user_init

        i:int = 0

        gl_journal = db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == inp_jnr) & (Gl_journal.activeflag == 0)).first()
        while None != gl_journal:

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == gl_journal.fibukonto)).first()

            gl_accthis = db_session.query(Gl_accthis).filter(
                     (Gl_accthis.fibukonto == gl_journal.fibukonto) & (Gl_accthis.year == curr_year)).first()

            if not gl_accthis:
                gl_accthis = Gl_accthis()
                db_session.add(gl_accthis)

                buffer_copy(gl_acct, gl_accthis)
                gl_accthis.year = curr_year


            gl_accthis.actual[curr_month - 1] = gl_accthis.actual[curr_month - 1] + gl_journal.debit - gl_journal.credit
            gl_acct.last_yr[curr_month - 1] = gl_acct.last_yr[curr_month - 1] + gl_journal.debit - gl_journal.credit

            if gl_acct.acc_type == 1:
                profit =  to_decimal(profit) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)

            elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                lost =  to_decimal(lost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

            elif gl_acct.acc_type == 3:
                for i in range(from_month,to_month + 1) :
                    gl_acct.actual[i - 1] = gl_acct.actual[i - 1] + gl_journal.debit - gl_journal.credit

            elif gl_acct.acc_type == 4:
                for i in range(from_month,to_month + 1) :
                    gl_acct.actual[i - 1] = gl_acct.actual[i - 1] + gl_journal.debit - gl_journal.credit
            gl_journal.activeflag = 1

            curr_recid = gl_journal._recid
            gl_journal = db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == inp_jnr) & (Gl_journal.activeflag == 0)).filter(Gl_journal._recid > curr_recid).first()


    def process_jouhdr():

        nonlocal closed, msg_str, lvcarea, curr_date, curr_month, curr_year, prev_month, from_month, to_month, pnl_acct, balance, profit, lost, i, htparam, gl_acct, gl_jouhdr, gl_journal, gl_accthis, bediener, res_history
        nonlocal pvilanguage, user_init

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum == curr_date)).first()
        while None != gl_jouhdr:
            gl_jouhdr.activeflag = 1

            curr_recid = gl_jouhdr._recid
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum == curr_date)).filter(Gl_jouhdr._recid > curr_recid).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    curr_date = htparam.fdate
    curr_year = get_year(curr_date)
    curr_month = 12
    prev_month = 11

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    from_month = 1
    to_month = get_month(htparam.fdate) - 1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 980)).first()

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == fchar)).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("P&L Last Year Adjustment Account not defined (Parameter 980).", lvcarea, "")

        return generate_output()

    if gl_acct.acc_type != 4:
        msg_str = msg_str + chr(2) + translateExtended ("P&L Last Year Adjustment Account has wrong type (Parameter 980).", lvcarea, "")

        return generate_output()
    pnl_acct = gl_acct.fibukonto

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum == curr_date)).first()
    while None != gl_jouhdr:
        balance =  to_decimal("0")

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
            balance =  to_decimal(balance) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

        if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
            msg_str = msg_str + chr(2) + translateExtended ("Not balanced Journals found (closing not possible).", lvcarea, "") + chr(10) + translateExtended ("Date : ", lvcarea, "") + to_string(gl_jouhdr.datum) + " - " + translateExtended ("RefNo : ", lvcarea, "") + gl_jouhdr.refno

            return generate_output()

        curr_recid = gl_jouhdr._recid
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum == curr_date)).filter(Gl_jouhdr._recid > curr_recid).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 983)).first()
    htparam.flogical = True

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum == curr_date)).order_by(Gl_jouhdr._recid).all():
        process_journal(gl_jouhdr.jnr)
    process_jouhdr()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 980)).first()

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == fchar)).first()
    gl_acct.last_yr[curr_month - 1] = gl_acct.last_yr[curr_month - 1] -\
            profit + lost


    for i in range(from_month,to_month + 1) :
        gl_acct.actual[i - 1] = gl_acct.actual[i - 1] - profit + lost

    gl_accthis = db_session.query(Gl_accthis).filter(
             (Gl_accthis.fibukonto == gl_acct.fibukonto) & (Gl_accthis.year == curr_year)).first()

    if not gl_accthis:
        gl_accthis = Gl_accthis()
        db_session.add(gl_accthis)

        buffer_copy(gl_acct, gl_accthis,except_fields=["actual","last_yr"])
        gl_accthis.year = curr_year


    gl_accthis.actual[curr_month - 1] = gl_accthis.actual[curr_month - 1] -\
            profit + lost

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Close Year Adjustment - " + to_string(curr_date)
    res_history.action = "G/L"


    pass
    closed = True

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 983)).first()
    htparam.flogical = False

    return generate_output()