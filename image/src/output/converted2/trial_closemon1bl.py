from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_acct, Gl_jouhdr, Gl_journal

def trial_closemon1bl(pvilanguage:int):
    msg_str = ""
    lvcarea:str = "closemonth"
    pnl_acct:str = ""
    balance:decimal = to_decimal("0.0")
    curr_date:date = None
    first_date:date = None
    err_acct:bool = False
    htparam = gl_acct = gl_jouhdr = gl_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, pnl_acct, balance, curr_date, first_date, err_acct, htparam, gl_acct, gl_jouhdr, gl_journal
        nonlocal pvilanguage

        return {"msg_str": msg_str}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()

    if (get_year(htparam.fdate) + 1) < get_year(curr_date):
        msg_str = msg_str + chr(2) + translateExtended ("Closing Year not yet done!", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 558)).first()
    first_date = htparam.fdate + timedelta(days=1)

    if htparam.fdate >= curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing date incorrect (Parameter 558).", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 979)).first()

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == fchar)).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("P&L Account not defined (Parameter 979).", lvcarea, "")

        return generate_output()
    pnl_acct = gl_acct.fibukonto

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).first()
    while None != gl_jouhdr:
        balance =  to_decimal("0")
        err_acct = False

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == gl_journal.fibukonto)).first()

            if not gl_acct:
                err_acct = True


            balance =  to_decimal(balance) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

        if err_acct :
            msg_str = translateExtended ("Chart of Account : ", lvcarea, "") + gl_journal.fibukonto + translateExtended (" not defined ", lvcarea, "")

            return generate_output()

        if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
            msg_str = msg_str + chr(2) + translateExtended ("Not balanced Journals found; trial not possible.", lvcarea, "") + chr(10) + translateExtended ("Date:", lvcarea, "") + " " + to_string(gl_jouhdr.datum) + " - " + translateExtended ("RefNo:", lvcarea, "") + " " + gl_jouhdr.refno

            return generate_output()

        curr_recid = gl_jouhdr._recid
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).filter(Gl_jouhdr._recid > curr_recid).first()

    return generate_output()