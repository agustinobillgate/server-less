from functions.additional_functions import *
import decimal
from models import Gl_main

g_list_list, G_list = create_model_like(Gl_main)

def glmain_admin_btn_exitbl( case_type:int, g_list_list:[G_list]):
    code_0 = False
    msg_str = ""
    success_flag = False
    lvcarea:str = "glmain_admin"
    gl_main = None

    g_list = gl_main1 = None
    Gl_main1 = Gl_main

    db_session = local_storage.db_session

    def generate_output():
        nonlocal code_0, msg_str, success_flag, lvcarea, gl_main
        nonlocal gl_main1


        nonlocal g_list, gl_main1
        global  g_list_list
        return {"code_0": code_0, "msg_str": msg_str, "success_flag": success_flag}

    def validate_it():

        nonlocal code_0, msg_str, success_flag, lvcarea, gl_main
        nonlocal gl_main1


        nonlocal g_list, gl_main1
        global g_list_list

        gl_main1 = db_session.query(Gl_main1).filter(
                (Gl_main1.code == g_list.code) &  (Gl_main1.nr != g_list.nr)).first()

        if gl_main1:
            msg_str = msg_str + chr(2) + translateExtended ("Other G/L Main Account with the same code exists.", lvcarea, "")
            code_0 = True

        gl_main1 = db_session.query(Gl_main1).filter(
                (Gl_main1.bezeich == g_list.bezeich) &  (Gl_main1.nr != g_list.nr)).first()

        if gl_main1:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Other G/L Main Account exists with the same description.", lvcarea, "")

    g_list = query(g_list_list, first=True)
    validate_it()

    if code_0:

        return generate_output()

    if case_type == 1:
        gl_main = Gl_main()
        db_session.add(gl_main)

        buffer_copy(g_list, gl_main)

        success_flag = True

    if case_type == 2:

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.nr == g_list.nr)).first()

        if gl_main:
            buffer_copy(g_list, gl_main)

        gl_main = db_session.query(Gl_main).first()

        success_flag = True

    return generate_output()