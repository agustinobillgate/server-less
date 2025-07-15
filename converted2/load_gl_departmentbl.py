#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_department

def load_gl_departmentbl():
    t_gl_department_data = []
    gl_department = None

    t_gl_department = None

    t_gl_department_data, T_gl_department = create_model_like(Gl_department)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_department_data, gl_department


        nonlocal t_gl_department
        nonlocal t_gl_department_data

        return {"t-gl-department": t_gl_department_data}

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_department = T_gl_department()
        t_gl_department_data.append(t_gl_department)

        buffer_copy(gl_department, t_gl_department)

    return generate_output()