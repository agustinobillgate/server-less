from functions.additional_functions import *
import decimal
from models import Gc_giro, Gl_acct

def gc_giroadmin_btn_gobl(pvilanguage:int, case_type:int, s_recid:int, user_init:str, g_list:[G_list]):
    msg_str = ""
    err_code = 0
    success_flag = False
    lvcarea:str = "gc_giroAdmin"
    gc_giro = gl_acct = None

    g_list = None

    g_list_list, G_list = create_model_like(Gc_giro, {"acctno":str, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_code, success_flag, lvcarea, gc_giro, gl_acct


        nonlocal g_list
        nonlocal g_list_list
        return {"msg_str": msg_str, "err_code": err_code, "success_flag": success_flag}

    def chk_gc():

        nonlocal msg_str, err_code, success_flag, lvcarea, gc_giro, gl_acct


        nonlocal g_list
        nonlocal g_list_list

        if case_type == 1:

            gc_giro = db_session.query(Gc_giro).filter(
                    (Gc_giro.bankname == g_list.bankname) &  (Gc_giro.gironum == g_list.gironum) &  (Gc_giro._recid != s_recid)).first()

        elif case_type == 2:

            gc_giro = db_session.query(Gc_giro).filter(
                    (Gc_giro.bankname == g_list.bankname) &  (Gc_giro.gironum == g_list.gironum)).first()

        if gc_giro:
            msg_str = msg_str + chr(2) + translateExtended ("Giro number already exists.", lvcarea, "")
            err_code = 1

            return

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == g_list.acctno)).first()

        if not gl_acct:
            msg_str = msg_str + chr(2) + translateExtended ("Account number not found.", lvcarea, "")
            err_code = 2

            return

    g_list = query(g_list_list, first=True)

    if case_type == 1:
        chk_gc()

        gc_giro = db_session.query(Gc_giro).filter(
                (Gc_giro._recid == s_recid)).first()
        buffer_copy(g_list, gc_giro)
        gc_giro.fibukonto = g_list.acctNo
        gc_giro.changed = get_current_date()
        gc_giro.CID = user_init

        gc_giro = db_session.query(Gc_giro).first()
        success_flag = True

    if case_type == 2:
        chk_gc()

        if err_code == 0:
            gc_giro = Gc_giro()
            db_session.add(gc_giro)

            buffer_copy(g_list, gc_giro)
            gc_giro.fibukonto = g_list.acctNo

            gc_giro = db_session.query(Gc_giro).first()
            success_flag = True

    return generate_output()