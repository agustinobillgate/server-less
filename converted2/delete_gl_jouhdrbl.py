#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr

def delete_gl_jouhdrbl(case_type:int, int1:int, int2:int, char1:string, date1:date):
    successflag = False
    gl_jouhdr = None

    t_gl_jouhdr = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gl_jouhdr
        nonlocal case_type, int1, int2, char1, date1


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_data

        return {"successflag": successflag}

    if case_type == 1:

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, char1)],"jnr": [(eq, int1)],"jtype": [(eq, int2)]})

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 2:

        gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, int1)]})

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True


    elif case_type == 3:

        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, int1)]})

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            pass
            successflag = True

    return generate_output()