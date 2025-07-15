#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_fstype

def read_gl_fstypebl(case_type:int, int1:int, char1:string, char2:string):
    t_gl_fstype_data = []
    gl_fstype = None

    t_gl_fstype = None

    t_gl_fstype_data, T_gl_fstype = create_model_like(Gl_fstype)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_fstype_data, gl_fstype
        nonlocal case_type, int1, char1, char2


        nonlocal t_gl_fstype
        nonlocal t_gl_fstype_data

        return {"t-gl-fstype": t_gl_fstype_data}

    def assign_it():

        nonlocal t_gl_fstype_data, gl_fstype
        nonlocal case_type, int1, char1, char2


        nonlocal t_gl_fstype
        nonlocal t_gl_fstype_data


        t_gl_fstype = T_gl_fstype()
        t_gl_fstype_data.append(t_gl_fstype)

        buffer_copy(gl_fstype, t_gl_fstype)


    if case_type == 1:

        gl_fstype = get_cache (Gl_fstype, {"nr": [(eq, int1)]})

        if gl_fstype:
            assign_it()
    elif case_type == 2:

        for gl_fstype in db_session.query(Gl_fstype).order_by(Gl_fstype.nr).all():
            assign_it()

    return generate_output()