#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_department

def load_gl_departmentbl():
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

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_department = T_gl_department()
        t_gl_department_list.append(t_gl_department)

        buffer_copy(gl_department, t_gl_department)

    return generate_output()