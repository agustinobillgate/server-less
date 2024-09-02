from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Bediener, Res_history

def delete_gl_jouhdr_1bl(case_type:int, int1:int, int2:int, char1:str, date1:date, user_init:str):
    successflag = False
    datum:date = None
    refno:str = ""
    bezeich:str = ""
    gl_jouhdr = bediener = res_history = None

    t_gl_jouhdr = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, datum, refno, bezeich, gl_jouhdr, bediener, res_history


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_list
        return {"successflag": successflag}

    if case_type == 1:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (func.lower(Gl_jouhdr.refno) == (char1).lower()) &  (Gl_jouhdr.jnr == int1) &  (Gl_jouhdr.jtype == int2)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)

            successflag = True


    elif case_type == 2:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr._recid == int1)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)

            successflag = True


    elif case_type == 3:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.jnr == int1)).first()

        if gl_jouhdr:
            datum = gl_jouhdr.datum
            refno = gl_jouhdr.refno
            bezeich = gl_jouhdr.bezeich


            db_session.delete(gl_jouhdr)

            successflag = True

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Journal, Date: " + to_string(datum) + ", refno: " + refno + ", Desc: " + bezeich
                res_history.action = "G/L"

                res_history = db_session.query(Res_history).first()


    return generate_output()