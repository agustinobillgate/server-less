from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_main

def read_gl_mainbl(case_type:int, int1:int, int2:int, char1:str, char2:str):
    t_gl_main_list = []
    gl_main = None

    t_gl_main = None

    t_gl_main_list, T_gl_main = create_model_like(Gl_main)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_main_list, gl_main


        nonlocal t_gl_main
        nonlocal t_gl_main_list
        return {"t-gl-main": t_gl_main_list}

    if case_type == 1:

        gl_main = db_session.query(Gl_main).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 2:

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.code == int1)).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 3:

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.nr == int1)).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 4:

        for gl_main in db_session.query(Gl_main).all():
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 5:

        gl_main = db_session.query(Gl_main).filter(
                (func.lower(Gl_main.bezeich) == (char1).lower()) &  (Gl_main.nr != int1)).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 6:

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.code == int1) &  (Gl_main.nr != int2)).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_list.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)

    return generate_output()