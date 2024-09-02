from functions.additional_functions import *
import decimal
from models import Gl_department

def read_gl_departmentbl(case_type:int, int1:int, int2:str, char1:str):
    t_gl_department_list = []
    gl_department = None

    t_gl_department = None

    t_gl_department_list, T_gl_department = create_model_like(Gl_department)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_department_list, gl_department


        nonlocal t_gl_department
        nonlocal t_gl_department_list
        return {"t-gl-department": t_gl_department_list}

    def assign_it():

        nonlocal t_gl_department_list, gl_department


        nonlocal t_gl_department
        nonlocal t_gl_department_list


        t_gl_department = T_gl_department()
        t_gl_department_list.append(t_gl_department)

        buffer_copy(gl_department, t_gl_department)

    if case_type == 1:

        gl_department = db_session.query(Gl_department).filter(
                (Gl_department.nr == int1)).first()

        if gl_department:
            assign_it()

    return generate_output()