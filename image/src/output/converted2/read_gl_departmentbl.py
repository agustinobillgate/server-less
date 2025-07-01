#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_department

def read_gl_departmentbl(case_type:int, int1:int, int2:string, char1:string):
    t_gl_department_list = []
    gl_department = None

    t_gl_department = None

    t_gl_department_list, T_gl_department = create_model_like(Gl_department)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_department_list, gl_department
        nonlocal case_type, int1, int2, char1


        nonlocal t_gl_department
        nonlocal t_gl_department_list

        return {"t-gl-department": t_gl_department_list}

    def assign_it():

        nonlocal t_gl_department_list, gl_department
        nonlocal case_type, int1, int2, char1


        nonlocal t_gl_department
        nonlocal t_gl_department_list


        t_gl_department = T_gl_department()
        t_gl_department_list.append(t_gl_department)

        buffer_copy(gl_department, t_gl_department)


    if case_type == 1:

        gl_department = get_cache (Gl_department, {"nr": [(eq, int1)]})

        if gl_department:
            assign_it()

    return generate_output()