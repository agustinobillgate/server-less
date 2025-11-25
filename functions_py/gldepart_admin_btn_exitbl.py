#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 25/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_department

g_list_data, G_list = create_model_like(Gl_department)

def gldepart_admin_btn_exitbl(g_list_data:[G_list], case_type:int):

    prepare_cache ([Gl_department])

    success_flag = False
    gl_department = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_department
        nonlocal case_type


        nonlocal g_list

        return {"success_flag": success_flag}

    def fill_gl_department():

        nonlocal success_flag, gl_department
        nonlocal case_type
        nonlocal g_list
        gl_department.nr = g_list.nr
        gl_department.bezeich = g_list.bezeich
        gl_department.fodept = g_list.fodept


    g_list = query(g_list_data, first=True)

    if case_type == 1:
        gl_department = Gl_department()
        db_session.add(gl_department)

        fill_gl_department()
        pass
        success_flag = True

    elif case_type == 2:
        # Rd, 25/11/2025, with_for_update added
        # gl_department = get_cache (Gl_department, {"nr": [(eq, g_list.nr)]})
        gl_department = db_session.query(Gl_department).filter(
                     (Gl_department.nr == g_list.nr)).with_for_update().first()

        if gl_department:
            fill_gl_department()
        pass
        pass
        success_flag = True

    return generate_output()