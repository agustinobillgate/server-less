from functions.additional_functions import *
import decimal
from models import Gc_piacct, Gl_acct

p_list_list, P_list = create_model_like(Gc_piacct)

def gc_piacct_btn_exitbl(p_list_list:[P_list], case_type:int, active_flag:bool):
    flag = 0
    flag2 = 0
    gc_piacct = gl_acct = None

    p_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, flag2, gc_piacct, gl_acct
        nonlocal case_type, active_flag


        nonlocal p_list
        nonlocal p_list_list
        return {"flag": flag, "flag2": flag2}

    def fill_new_gc_piacct():

        nonlocal flag, flag2, gc_piacct, gl_acct
        nonlocal case_type, active_flag


        nonlocal p_list
        nonlocal p_list_list


        gc_piacct.nr = p_list.nr
        gc_piacct.fibukonto = p_list.fibukonto
        gc_piacct.bezeich = p_list.bezeich
        gc_piacct.activeflag = to_int(not active_flag)


        pass


    p_list = query(p_list_list, first=True)

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == p_list.fibukonto)).first()

    if not gl_acct:
        flag = 1

        if p_list.bezeich == "":
            flag2 = 1

            return generate_output()

    if case_type == 1:
        gc_piacct = Gc_piacct()
        db_session.add(gc_piacct)

        fill_new_gc_piacct()

    elif case_type == 2:

        gc_piacct = db_session.query(Gc_piacct).filter(
                 (Gc_piacct.nr == p_list.nr)).first()

        if gc_piacct:
            gc_piacct.fibukonto = p_list.fibukonto
            gc_piacct.bezeich = p_list.bezeich
            gc_piacct.activeflag = to_int(not active_flag)


            pass

    return generate_output()