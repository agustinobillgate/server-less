from functions.additional_functions import *
import decimal
from models import Gl_fstype

def read_gl_fstypebl(case_type:int, int1:int, char1:str, char2:str):
    t_gl_fstype_list = []
    gl_fstype = None

    t_gl_fstype = None

    t_gl_fstype_list, T_gl_fstype = create_model_like(Gl_fstype)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_fstype_list, gl_fstype


        nonlocal t_gl_fstype
        nonlocal t_gl_fstype_list
        return {"t-gl-fstype": t_gl_fstype_list}

    def assign_it():

        nonlocal t_gl_fstype_list, gl_fstype


        nonlocal t_gl_fstype
        nonlocal t_gl_fstype_list


        t_gl_fstype = T_gl_fstype()
        t_gl_fstype_list.append(t_gl_fstype)

        buffer_copy(gl_fstype, t_gl_fstype)

    if case_type == 1:

        gl_fstype = db_session.query(Gl_fstype).filter(
                (Gl_fstype.nr == int1)).first()

        if gl_fstype:
            assign_it()
    elif case_type == 2:

        for gl_fstype in db_session.query(Gl_fstype).all():
            assign_it()

    return generate_output()