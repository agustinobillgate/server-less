from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_jouhdr, Gl_journal, Bediener, Res_history

def delete_gl_adjustment_allbl(refno:str, jnr:int, bezeich:str, user_init:str, to_date:date):
    flag = False
    msg = ""
    close_year:date = None
    htparam = gl_jouhdr = gl_journal = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg, close_year, htparam, gl_jouhdr, gl_journal, bediener, res_history
        nonlocal refno, jnr, bezeich, user_init, to_date

        return {"flag": flag, "msg": msg}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.jnr == jnr)).first()

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 0 and gl_jouhdr.jtype == 0:

            if gl_jouhdr.datum == to_date:

                for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                    db_session.delete(gl_journal)
                db_session.delete(gl_jouhdr)
                flag = True


            else:
                flag = False


                msg = "Wrong Year Closing Date."

                return generate_output()

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Deleted Last Year Adjustment With Reference No: " +\
                refno + "|Desc: " + bezeich + "|By:" + bediener.username
        res_history.action = "JournalTransactionDelete"


        pass

    return generate_output()