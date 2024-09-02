from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Gl_acct, Gl_journal

def closemonth1bl(pvilanguage:int):
    curr_date = None
    msg_str = ""
    curr_closeyr:int = 0
    balance:decimal = 0
    pnl_acct:str = ""
    first_date:date = None
    bom_597:date = None
    end_of_month:date = None
    param269:date = None
    param1003:date = None
    param1014:date = None
    param1035:date = None
    param1118:date = None
    param1123:date = None
    lvcarea:str = "closemonth"
    htparam = gl_jouhdr = gl_acct = gl_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, msg_str, curr_closeyr, balance, pnl_acct, first_date, bom_597, end_of_month, param269, param1003, param1014, param1035, param1118, param1123, lvcarea, htparam, gl_jouhdr, gl_acct, gl_journal


        return {"curr_date": curr_date, "msg_str": msg_str}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 269)).first()
    param269 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1003)).first()
    param1003 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1014)).first()
    param1014 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1035)).first()
    param1035 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1118)).first()
    param1118 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1123)).first()
    param1123 = htparam.fdate

    if param269 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 269.", lvcarea, "")

        return generate_output()

    elif param1003 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 1003.", lvcarea, "")

        return generate_output()

    elif param1014 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 1014.", lvcarea, "")

        return generate_output()

    elif param1035 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 1035.", lvcarea, "")

        return generate_output()

    elif param1118 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 1118.", lvcarea, "")

        return generate_output()

    elif param1123 < curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing month not possible, please check Parameter 1123.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    first_date = fdate + timedelta(days=1)

    if htparam.fdate >= curr_date:
        msg_str = msg_str + chr(2) + translateExtended ("Closing date incorrect (Parameter 558).", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    curr_closeyr = get_year(htparam.fdate) + 1

    if get_year(curr_date) > curr_closeyr:
        msg_str = msg_str + chr(2) + translateExtended ("Closing Year has not been done yet.", lvcarea, "")

        return generate_output()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.batch) &  (Gl_jouhdr.datum <= curr_date)).first()

    if gl_jouhdr:
        msg_str = msg_str + chr(2) + translateExtended ("Batch journal(s) still exists, closing not possible.", lvcarea, "") + chr(10) + to_string(gl_jouhdr.datum) + " - " + gl_jouhdr.refno

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
            (Gl_jouhdr.activeflag == 1) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).first()

    if gl_jouhdr:
        msg_str = msg_str + chr(2) + translateExtended ("Closed Journal found! Re_check it.", lvcarea, "")

        return generate_output()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).first()
    while None != gl_jouhdr:
        balance = 0

        for gl_journal in db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == gl_jouhdr.jnr)).all():
            balance = balance + gl_journal.debit - gl_journal.credit

        if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
            msg_str = msg_str + chr(2) + translateExtended ("Not balanced Journals found (closing not possible).", lvcarea, "") + chr(10) + translateExtended ("Date : ", lvcarea, "") + to_string(gl_jouhdr.datum) + " - " + translateExtended ("RefNo : ", lvcarea, "") + gl_jouhdr.refno

            return generate_output()

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).first()

    return generate_output()