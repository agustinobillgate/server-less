#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr

def read_gl_jouhdrbl(case_type:int, int1:int, int2:int, char1:string, date1:date):
    t_gl_jouhdr_data = []
    gl_jouhdr = None

    t_gl_jouhdr = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_jouhdr_data, gl_jouhdr
        nonlocal case_type, int1, int2, char1, date1


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_data

        return {"t-gl-jouhdr": t_gl_jouhdr_data}

    if case_type == 1:

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, char1)],"jtype": [(eq, int1)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 2:

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, char1)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 3:

        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, int1)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 4:

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == int1)).order_by(Gl_jouhdr._recid).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 5:

        gl_jouhdr = get_cache (Gl_jouhdr, {"jtype": [(eq, int1)],"datum": [(gt, date1)],"activeflag": [(eq, int2)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)
    elif case_type == 6:

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, char1)],"datum": [(eq, date1)],"batch": [(eq, False)],"activeflag": [(eq, int2)]})

        if gl_jouhdr:
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)

    return generate_output()