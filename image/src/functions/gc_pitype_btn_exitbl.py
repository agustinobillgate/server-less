from functions.additional_functions import *
import decimal
from models import Gc_pitype

def gc_pitype_btn_exitbl(case_type:int, active_flag:bool, p_list:[P_list]):
    return_it = False
    success_flag = False
    gc_pitype = None

    p_list = gc_pitype1 = None

    p_list_list, P_list = create_model_like(Gc_pitype)

    Gc_pitype1 = Gc_pitype

    db_session = local_storage.db_session

    def generate_output():
        nonlocal return_it, success_flag, gc_pitype
        nonlocal gc_pitype1


        nonlocal p_list, gc_pitype1
        nonlocal p_list_list
        return {"return_it": return_it, "success_flag": success_flag}

    def chek_p_list():

        nonlocal return_it, success_flag, gc_pitype
        nonlocal gc_pitype1


        nonlocal p_list, gc_pitype1
        nonlocal p_list_list


        Gc_pitype1 = Gc_pitype

        gc_pitype1 = db_session.query(Gc_pitype1).filter(
                (Gc_pitype1.bezeich == p_list.bezeich) &  (Gc_pitype1.nr != p_list.nr)).first()

        if gc_pitype1 and gc_pitype1.bezeich != "":
            return_it = True

            return

    def fill_new_gc_pitype():

        nonlocal return_it, success_flag, gc_pitype
        nonlocal gc_pitype1


        nonlocal p_list, gc_pitype1
        nonlocal p_list_list


        gc_pitype.nr = p_list.nr
        gc_pitype.bezeich = p_list.bezeich
        gc_pitype.activeflag = to_int(not active_flag)


    p_list = query(p_list_list, first=True)
    chek_p_list()

    if return_it:

        return generate_output()

    if case_type == 1:
        gc_pitype = Gc_pitype()
        db_session.add(gc_pitype)

        fill_new_gc_pitype()
        success_flag = True

    elif case_type == 2:

        gc_pitype = db_session.query(Gc_pitype).filter(
                (Gc_pitype.nr == p_list.nr)).first()

        if gc_pitype:
            fill_new_gc_pitype()
            success_flag = True

    return generate_output()