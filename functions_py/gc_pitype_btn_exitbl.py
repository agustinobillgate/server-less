#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pitype

p_list_data, P_list = create_model_like(Gc_pitype)

def gc_pitype_btn_exitbl(case_type:int, active_flag:bool, p_list_data):

    prepare_cache ([Gc_pitype])

    return_it = False
    success_flag = False
    gc_pitype = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal return_it, success_flag, gc_pitype
        nonlocal case_type, active_flag


        nonlocal p_list

        return {"return_it": return_it, "success_flag": success_flag}

    def chek_p_list():

        nonlocal return_it, success_flag, gc_pitype
        nonlocal case_type, active_flag


        nonlocal p_list

        gc_pitype1 = None
        Gc_pitype1 =  create_buffer("Gc_pitype1",Gc_pitype)

        gc_pitype1 = get_cache (Gc_pitype, {"bezeich": [(eq, p_list.bezeich)],"nr": [(ne, p_list.nr)]})

        if gc_pitype1 and gc_pitype1.bezeich != "":
            return_it = True

            return


    def fill_new_gc_pitype():

        nonlocal return_it, success_flag, gc_pitype
        nonlocal case_type, active_flag


        nonlocal p_list


        gc_pitype.nr = p_list.nr
        gc_pitype.bezeich = p_list.bezeich
        gc_pitype.activeflag = to_int(not active_flag)


        pass


    p_list = query(p_list_data, first=True)
    chek_p_list()

    if return_it:

        return generate_output()

    if case_type == 1:
        gc_pitype = Gc_pitype()
        db_session.add(gc_pitype)

        fill_new_gc_pitype()
        success_flag = True

    elif case_type == 2:

        # gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, p_list.nr)]})
        gc_pitype = db_session.query(Gc_pitype).filter(
                 (Gc_pitype.nr == p_list.nr)).with_for_update().first()

        if gc_pitype:
            fill_new_gc_pitype()
            success_flag = True

    return generate_output()
