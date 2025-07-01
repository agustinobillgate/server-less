#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_main

g_list_list, G_list = create_model_like(Gl_main)

def glmain_admin_btn_exitbl(pvilanguage:int, case_type:int, g_list_list:[G_list]):
    code_0 = False
    msg_str = ""
    success_flag = False
    lvcarea:string = "glmain-admin"
    gl_main = None

    g_list = gl_main1 = None

    Gl_main1 = create_buffer("Gl_main1",Gl_main)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal code_0, msg_str, success_flag, lvcarea, gl_main
        nonlocal pvilanguage, case_type
        nonlocal gl_main1


        nonlocal g_list, gl_main1

        return {"code_0": code_0, "msg_str": msg_str, "success_flag": success_flag}

    def validate_it():

        nonlocal code_0, msg_str, success_flag, lvcarea, gl_main
        nonlocal pvilanguage, case_type
        nonlocal gl_main1


        nonlocal g_list, gl_main1

        gl_main1 = db_session.query(Gl_main1).filter(
                 (Gl_main1.code == g_list.code) & (Gl_main1.nr != g_list.nr)).first()

        if gl_main1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Other G/L Main Account with the same code exists.", lvcarea, "")
            code_0 = True

        gl_main1 = db_session.query(Gl_main1).filter(
                 (Gl_main1.bezeich == g_list.bezeich) & (Gl_main1.nr != g_list.nr)).first()

        if gl_main1:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Other G/L Main Account exists with the same description.", lvcarea, "")


    g_list = query(g_list_list, first=True)
    validate_it()

    if code_0:

        return generate_output()

    if case_type == 1:
        gl_main = Gl_main()
        db_session.add(gl_main)

        buffer_copy(g_list, gl_main)
        pass
        success_flag = True

    if case_type == 2:

        gl_main = get_cache (Gl_main, {"nr": [(eq, g_list.nr)]})

        if gl_main:
            buffer_copy(g_list, gl_main)
        pass
        pass
        success_flag = True

    return generate_output()