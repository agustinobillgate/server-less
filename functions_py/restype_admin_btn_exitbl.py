#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Sourccod

p_list_data, P_list = create_model_like(Sourccod)

def restype_admin_btn_exitbl(p_list_data:[P_list], case_type:int, active_flag:bool):

    prepare_cache ([Sourccod])

    success_flag = False
    sourccod = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, sourccod
        nonlocal case_type, active_flag


        nonlocal p_list

        return {"success_flag": success_flag}

    def fill_new_sourccod():

        nonlocal success_flag, sourccod
        nonlocal case_type, active_flag


        nonlocal p_list


        sourccod.source_code = p_list.source_code
        sourccod.bemerkung = p_list.bemerkung
        sourccod.bezeich = p_list.bezeich
        sourccod.betriebsnr = to_int(not active_flag)


        pass


    p_list = query(p_list_data, first=True)

    if case_type == 1:
        sourccod = Sourccod()
        db_session.add(sourccod)

        fill_new_sourccod()
        success_flag = True

    elif case_type == 2:

        # sourccod = get_cache (Sourccod, {"source_code": [(eq, p_list.source_code)]})
        sourccod = db_session.query(Sourccod).filter(
                 (Sourccod.source_code == p_list.source_code)).with_for_update().first()

        if sourccod:
            fill_new_sourccod()
        success_flag = True

    return generate_output()