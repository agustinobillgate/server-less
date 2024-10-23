from functions.additional_functions import *
import decimal
from models import Gl_fstype

g_list_list, G_list = create_model_like(Gl_fstype)

def fstype_adminbl(g_list_list:[G_list]):
    gl_fstype = None

    g_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_fstype


        nonlocal g_list
        nonlocal g_list_list
        return {"g-list": g_list_list}

    g_list = query(g_list_list, first=True)

    if not g_list:

        return generate_output()

    gl_fstype = db_session.query(Gl_fstype).filter(
             (Gl_fstype.nr == g_list.nr)).first()

    if not gl_fstype:
        gl_fstype = Gl_fstype()
    db_session.add(gl_fstype)

    buffer_copy(g_list, gl_fstype)

    return generate_output()