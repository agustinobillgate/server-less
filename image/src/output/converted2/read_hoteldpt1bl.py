#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def read_hoteldpt1bl(case_type:int, int1:int, int2:int, char1:string):
    t_hoteldpt_list = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hoteldpt_list, hoteldpt
        nonlocal case_type, int1, int2, char1


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"t-hoteldpt": t_hoteldpt_list}

    def assign_it():

        nonlocal t_hoteldpt_list, hoteldpt
        nonlocal case_type, int1, int2, char1


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list


        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)


    if case_type == 1:

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, int1)]})

        if hoteldpt:
            assign_it()
    elif case_type == 2:

        hoteldpt = get_cache (Hoteldpt, {"depart": [(eq, char1)],"num": [(ne, int1)]})

        if hoteldpt:
            assign_it()

    return generate_output()