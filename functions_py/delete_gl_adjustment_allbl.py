#using conversion tools version: 1.0.0.117
#----------------------------------------------------------------------
# Rd, 25/11/2025, add .with_for_update
#----------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Gl_journal, Bediener, Res_history

def delete_gl_adjustment_allbl(refno:string, jnr:int, bezeich:string, user_init:string, to_date:date):

    prepare_cache ([Htparam, Bediener, Res_history])

    flag = False
    msg = ""
    close_year:date = None
    htparam = gl_jouhdr = gl_journal = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg, close_year, htparam, gl_jouhdr, gl_journal, bediener, res_history
        nonlocal refno, jnr, bezeich, user_init, to_date

        return {"flag": flag, "msg": msg}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    # Rd, 25/11/2025, add .with_for_update
    # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
    gl_jouhdr = db_session.query(Gl_jouhdr).filter(Gl_jouhdr.jnr == jnr).with_for_update().first()

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 0 and gl_jouhdr.jtype == 0:

            if gl_jouhdr.datum == to_date:
                # Rd, 25/11/2025, add .with_for_update
                # for gl_journal in db_session.query(Gl_journal).filter(
                #          (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).with_for_update().order_by(Gl_journal._recid).all():
                    db_session.delete(gl_journal)
                pass
                db_session.delete(gl_jouhdr)
                flag = True


            else:
                flag = False


                msg = "Wrong Year Closing Date."

                return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

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
        pass

    return generate_output()