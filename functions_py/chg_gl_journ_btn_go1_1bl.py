#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 25/11/2025, add with_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr, Bediener, Res_history

def chg_gl_journ_btn_go1_1bl(t_refno:string, t_bezeich:string, t_recid:int, user_init:string):

    prepare_cache ([Gl_jouhdr, Bediener, Res_history])

    refno:string = ""
    bez:string = ""
    datum:date = None
    gl_jouhdr = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal refno, bez, datum, gl_jouhdr, bediener, res_history
        nonlocal t_refno, t_bezeich, t_recid, user_init

        return {}

    # Rd, 25/11/2025, add with_for_update
    # gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, t_recid)]})
    gl_jouhdr = db_session.query(Gl_jouhdr).filter(Gl_jouhdr._recid == t_recid).with_for_update().first()
    refno = gl_jouhdr.refno
    bez = gl_jouhdr.bezeich
    datum = gl_jouhdr.datum

    if t_refno != "":
        pass
        gl_jouhdr.refno = t_refno


        pass

    if t_bezeich != "":
        pass
        gl_jouhdr.bezeich = t_bezeich


        pass

    if gl_jouhdr.refno.lower()  != (refno).lower() :

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", refno From: " + refno + " To: " + gl_jouhdr.refno
            res_history.action = "G/L"


            pass
            pass

    if gl_jouhdr.bezeich.lower()  != (bez).lower() :

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Journal, Date: " + to_string(datum) + ", Desc From: " + bez + " To: " + gl_jouhdr.bezeich
            res_history.action = "G/L"


            pass
            pass

    return generate_output()