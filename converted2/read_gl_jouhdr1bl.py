#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr

def read_gl_jouhdr1bl(case_type:int, int1:int, int2:int, char1:string, date1:date, date2:date):
    t_gl_jouhdr_data = []
    gl_jouhdr = None

    t_gl_jouhdr = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_jouhdr_data, gl_jouhdr
        nonlocal case_type, int1, int2, char1, date1, date2


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_data

        return {"t-gl-jouhdr": t_gl_jouhdr_data}

    if case_type == 1:

        gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, int1)],"datum": [(le, date2),(ge, date1)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 2:

        gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(ge, date1),(le, date2)],"activeflag": [(eq, int1)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)

    return generate_output()