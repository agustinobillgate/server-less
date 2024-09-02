from functions.additional_functions import *
import decimal
from datetime import date, timedelta
from models import Htparam, Gl_acct, Gl_jouhdr, Gl_journal

def trial_closemon1bl(pvilanguage:int):
    msg_str = ""
    lvcarea:str = "closemonth"
    pnl_acct:str = ""
    balance:decimal = 0
    curr_date:date = None
    first_date:date = None
    err_acct:bool = False
    htparam = gl_acct = gl_jouhdr = gl_journal = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, pnl_acct, balance, curr_date, first_date, err_acct, htparam, gl_acct, gl_jouhdr, gl_journal
        return {"msg_str": msg_str}

    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 597)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 795)).first()

    if (get_year(htparam.fdate) + 1) < get_year(curr_date):
        msg_str = msg_str + chr(2) + "Closing Year not yet done!"

        return generate_output()

    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 558)).first()
    first_date = htparam.fdate + timedelta(days=1)

    if htparam.fdate >= curr_date:
        msg_str = msg_str + chr(2) + "Closing date incorrect (Parameter 558)."
        return generate_output()

    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 979)).first()
    gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == htparam.fchar)).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + "P&L Account not defined (Parameter 979)."

        return generate_output()
    pnl_acct = gl_acct.fibukonto

    for  gl_jouhdr in  db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.activeflag == 0) and  \
            (Gl_jouhdr.datum >= first_date) and  \
            (Gl_jouhdr.datum <= curr_date)).all():
        
        balance = 0
        err_acct = False
        
        for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr)).all():
            gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto)).first()

            if not gl_acct:
                err_acct = True

            balance = balance + gl_journal.debit - gl_journal.credit

        if err_acct :
            msg_str = "Chart of Account : " + gl_journal.fibukonto + " not defined "
            return generate_output()

        if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
            msg_str = msg_str \
                        + chr(2) + "Not balanced Journals found; trial not possible." \
                        + chr(10) + "Date: " + to_string(gl_jouhdr.datum) \
                        + " - RefNo:" + gl_jouhdr.refno
            return generate_output()

        # gl_jouhdr = db_session.query(Gl_jouhdr)\
        #         .filter((Gl_jouhdr.activeflag == 0) and  \
        #                 (Gl_jouhdr.datum >= first_date) and  \
        #                 (Gl_jouhdr.datum <= curr_date)) \
        #         .first()

    # while None != gl_jouhdr:
    #     balance = 0
    #     err_acct = False
    #     print("GL:", gl_jouhdr.jnr)
    #     for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr)).all():
    #         gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto)).first()

    #         if not gl_acct:
    #             err_acct = True

    #         balance = balance + gl_journal.debit - gl_journal.credit

    #     if err_acct :
    #         msg_str = "Chart of Account : " + gl_journal.fibukonto + " not defined "
    #         return generate_output()

    #     if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
    #         msg_str = msg_str \
    #                     + chr(2) + "Not balanced Journals found; trial not possible." \
    #                     + chr(10) + "Date: " + to_string(gl_jouhdr.datum) \
    #                     + " - RefNo:" + gl_jouhdr.refno
    #         return generate_output()

    #     gl_jouhdr = db_session.query(Gl_jouhdr)\
    #             .filter((Gl_jouhdr.activeflag == 0) and  \
    #                     (Gl_jouhdr.datum >= first_date) and  \
    #                     (Gl_jouhdr.datum <= curr_date)) \
    #             .first()

    return generate_output()