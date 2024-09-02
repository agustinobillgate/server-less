from functions.additional_functions import *
import decimal
from models import Sourccod

def restype_admin_btn_exitbl(p_list:[P_list], case_type:int, active_flag:bool):
    success_flag = False
    sourccod = None

    p_list = None

    p_list_list, P_list = create_model_like(Sourccod)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, sourccod


        nonlocal p_list
        nonlocal p_list_list
        return {"success_flag": success_flag}

    def fill_new_sourccod():

        nonlocal success_flag, sourccod


        nonlocal p_list
        nonlocal p_list_list


        sourccod.source_code = p_list.source_code
        sourccod.bemerk = p_list.bemerk
        sourccod.bezeich = p_list.bezeich
        sourccod.betriebsnr = to_int(not active_flag)


    p_list = query(p_list_list, first=True)

    if case_type == 1:
        sourccod = Sourccod()
        db_session.add(sourccod)

        fill_new_sourccod()
        success_flag = True

    elif case_type == 2:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == p_list.source_code)).first()

        if sourccod:
            fill_new_sourccod()
        success_flag = True

    return generate_output()