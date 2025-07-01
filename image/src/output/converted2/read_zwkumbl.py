#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zwkum

def read_zwkumbl(case_type:int, int1:int, int2:int, int3:int, char1:string, char2:string, log1:bool, log2:bool):
    t_zwkum_list = []
    zwkum = None

    t_zwkum = None

    t_zwkum_list, T_zwkum = create_model_like(Zwkum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zwkum_list, zwkum
        nonlocal case_type, int1, int2, int3, char1, char2, log1, log2


        nonlocal t_zwkum
        nonlocal t_zwkum_list

        return {"t-zwkum": t_zwkum_list}

    def assign_it():

        nonlocal t_zwkum_list, zwkum
        nonlocal case_type, int1, int2, int3, char1, char2, log1, log2


        nonlocal t_zwkum
        nonlocal t_zwkum_list


        t_zwkum = T_zwkum()
        t_zwkum_list.append(t_zwkum)

        buffer_copy(zwkum, t_zwkum)


    if case_type == 1:

        zwkum = get_cache (Zwkum, {"zknr": [(eq, int1)],"departement": [(eq, int2)]})

        if zwkum:
            assign_it()
    elif case_type == 2:

        for zwkum in db_session.query(Zwkum).filter(
                 (Zwkum.departement == int1)).order_by(Zwkum._recid).all():
            assign_it()
    elif case_type == 3:

        zwkum = get_cache (Zwkum, {"zknr": [(ne, int1)],"departement": [(eq, int2)],"bezeich": [(eq, char1)]})

        if zwkum:
            assign_it()

    return generate_output()