from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr

def delete_gl_jouhdrbl(case_type:int, int1:int, int2:int, char1:str, date1:date):
    successflag = False
    gl_jouhdr = None

    t_gl_jouhdr = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gl_jouhdr
        nonlocal case_type, int1, int2, char1, date1


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_list
        return {"successflag": successflag}

    if case_type == 1:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (func.lower(Gl_jouhdr.refno) == (char1).lower()) & (Gl_jouhdr.jnr == int1) & (Gl_jouhdr.jtype == int2)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 2:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr._recid == int1)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 3:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.jnr == int1)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True

    return generate_output()