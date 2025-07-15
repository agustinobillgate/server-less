#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_giro, Gl_acct

g_list_data, G_list = create_model_like(Gc_giro, {"acctno":string, "s_recid":int})

def gc_giroadmin_btn_gobl(pvilanguage:int, case_type:int, s_recid:int, user_init:string, g_list_data:[G_list]):

    prepare_cache ([Gc_giro])

    msg_str = ""
    err_code = 0
    success_flag = False
    lvcarea:string = "gc-giroAdmin"
    gc_giro = gl_acct = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_code, success_flag, lvcarea, gc_giro, gl_acct
        nonlocal pvilanguage, case_type, s_recid, user_init


        nonlocal g_list

        return {"msg_str": msg_str, "err_code": err_code, "success_flag": success_flag}

    def chk_gc():

        nonlocal msg_str, err_code, success_flag, lvcarea, gc_giro, gl_acct
        nonlocal pvilanguage, case_type, s_recid, user_init


        nonlocal g_list

        if case_type == 1:

            gc_giro = get_cache (Gc_giro, {"bankname": [(eq, g_list.bankname)],"gironum": [(eq, g_list.gironum)],"_recid": [(ne, s_recid)]})

        elif case_type == 2:

            gc_giro = get_cache (Gc_giro, {"bankname": [(eq, g_list.bankname)],"gironum": [(eq, g_list.gironum)]})

        if gc_giro:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Giro number already exists.", lvcarea, "")
            err_code = 1

            return

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.acctno)]})

        if not gl_acct:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Account number not found.", lvcarea, "")
            err_code = 2

            return


    g_list = query(g_list_data, first=True)

    if case_type == 1:
        chk_gc()

        gc_giro = get_cache (Gc_giro, {"_recid": [(eq, s_recid)]})
        buffer_copy(g_list, gc_giro)
        gc_giro.fibukonto = g_list.acctno
        gc_giro.changed = get_current_date()
        gc_giro.cid = user_init


        pass
        success_flag = True

    if case_type == 2:
        chk_gc()

        if err_code == 0:
            gc_giro = Gc_giro()
            db_session.add(gc_giro)

            buffer_copy(g_list, gc_giro)
            gc_giro.fibukonto = g_list.acctno


            pass
            success_flag = True

    return generate_output()