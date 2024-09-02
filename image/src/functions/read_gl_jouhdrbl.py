from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr

def read_gl_jouhdrbl(case_type:int, int1:int, int2:int, char1:str, date1:date):
    t_gl_jouhdr_list = []
    gl_jouhdr = None

    t_gl_jouhdr = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_jouhdr_list, gl_jouhdr


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_list
        return {"t-gl-jouhdr": t_gl_jouhdr_list}

    if case_type == 1:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (func.lower(Gl_jouhdr.refno) == (char1).lower()) &  (Gl_jouhdr.jtype == int1)).first()

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 2:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (func.lower(Gl_jouhdr.refno) == (char1).lower())).first()

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 3:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.jnr == int1)).first()

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 4:

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.activeflag == int1)).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 5:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.jtype == int1) &  (Gl_jouhdr.datum > date1) &  (Gl_jouhdr.activeflag == int2)).first()

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 6:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (func.lower(Gl_jouhdr.refno) == (char1).lower()) &  (Gl_jouhdr.datum == date1) &  (Gl_jouhdr.batch == False) &  (Gl_jouhdr.activeflag == int2)).first()

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)

    return generate_output()