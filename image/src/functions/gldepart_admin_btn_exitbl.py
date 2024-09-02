from functions.additional_functions import *
import decimal
from models import Gl_department
g_list_list, G_list = create_model_like(Gl_department)
g_list = None

def gldepart_admin_btn_exitbl(g_list:[G_list], case_type:int):
    success_flag = False
    gl_department = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_department


        nonlocal g_list
        global g_list_list
        return {"success_flag": success_flag}

    def fill_gl_department():

        nonlocal success_flag, gl_department


        global g_list
        global g_list_list
        if g_list is not None:
            gl_department.nr = g_list.nr
            gl_department.bezeich = g_list.bezeich
            gl_department.fodept = g_list.fodept

    g_list = query(g_list_list, first=True)

    if case_type == 1:
        gl_department = Gl_department()
        db_session.add(gl_department)

        fill_gl_department()

        success_flag = True

    elif case_type == 2:

        gl_department = db_session.query(Gl_department).filter(
                (Gl_department.nr == g_list.nr)).first()

        if gl_department:
            fill_gl_department()

        gl_department = db_session.query(Gl_department).first()

        success_flag = True

    return generate_output()