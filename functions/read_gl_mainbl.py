#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_main

def read_gl_mainbl(case_type:int, int1:int, int2:int, char1:string, char2:string):
    t_gl_main_data = []
    gl_main = None

    t_gl_main = None

    t_gl_main_data, T_gl_main = create_model_like(Gl_main)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_main_data, gl_main
        nonlocal case_type, int1, int2, char1, char2


        nonlocal t_gl_main
        nonlocal t_gl_main_data

        return {"t-gl-main": t_gl_main_data}

    if case_type == 1:

        gl_main = db_session.query(Gl_main).first()

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 2:

        gl_main = get_cache (Gl_main, {"code": [(eq, int1)]})

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 3:

        gl_main = get_cache (Gl_main, {"nr": [(eq, int1)]})

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 4:

        for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 5:

        gl_main = get_cache (Gl_main, {"bezeich": [(eq, char1)],"nr": [(ne, int1)]})

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)
    elif case_type == 6:

        gl_main = get_cache (Gl_main, {"code": [(eq, int1)],"nr": [(ne, int2)]})

        if gl_main:
            t_gl_main = T_gl_main()
            t_gl_main_data.append(t_gl_main)

            buffer_copy(gl_main, t_gl_main)

    return generate_output()