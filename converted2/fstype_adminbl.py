#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_fstype

g_list_data, G_list = create_model_like(Gl_fstype)

def fstype_adminbl(g_list_data:[G_list]):
    gl_fstype = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_fstype


        nonlocal g_list

        return {"g-list": g_list_data}

    g_list = query(g_list_data, first=True)

    if not g_list:

        return generate_output()

    gl_fstype = get_cache (Gl_fstype, {"nr": [(eq, g_list.nr)]})

    if not gl_fstype:
        gl_fstype = Gl_fstype()
        db_session.add(gl_fstype)

    buffer_copy(g_list, gl_fstype)

    return generate_output()