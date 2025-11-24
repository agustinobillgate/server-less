#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Bediener, Res_history

def delete_gl_jouhdr_1bl(case_type:int, int1:int, int2:int, char1:string, date1:date, user_init:string):

    prepare_cache ([Bediener, Res_history])

    successflag = False
    datum:date = None
    refno:string = ""
    bezeich:string = ""
    gl_jouhdr = bediener = res_history = None

    t_gl_jouhdr = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, datum, refno, bezeich, gl_jouhdr, bediener, res_history
        nonlocal case_type, int1, int2, char1, date1, user_init


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_data

        return {"successflag": successflag}

    if case_type == 1:
        # Rd, 24/11/2025, get gl_jouhdr dengan for update
        # gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, char1)],"jnr": [(eq, int1)],"jtype": [(eq, int2)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.refno == char1) &
                     (Gl_jouhdr.jnr == int1) &
                     (Gl_jouhdr.jtype == int2)).with_for_update().first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 2:
        # Rd, 24/11/2025, get gl_jouhdr dengan for update
        # gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, int1)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr._recid == int1)).with_for_update().first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 3:
        # Rd, 24/11/2025, get gl_jouhdr dengan for update
        # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, int1)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.jnr == int1)).with_for_update().first()
        if gl_jouhdr:
            datum = gl_jouhdr.datum
            refno = gl_jouhdr.refno
            bezeich = gl_jouhdr.bezeich


            db_session.delete(gl_jouhdr)
            pass
            successflag = True

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Journal, Date: " + to_string(datum) + ", refno: " + refno + ", Desc: " + bezeich
                res_history.action = "G/L"


                pass
                pass

    return generate_output()