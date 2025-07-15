#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Ekum

def read_ekumbl(case_type:int, int1:int, int2:int, char1:string, char2:string):
    t_ekum_data = []
    ekum = None

    t_ekum = None

    t_ekum_data, T_ekum = create_model_like(Ekum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ekum_data, ekum
        nonlocal case_type, int1, int2, char1, char2


        nonlocal t_ekum
        nonlocal t_ekum_data

        return {"t-ekum": t_ekum_data}

    def assign_it():

        nonlocal t_ekum_data, ekum
        nonlocal case_type, int1, int2, char1, char2


        nonlocal t_ekum
        nonlocal t_ekum_data


        t_ekum = T_ekum()
        t_ekum_data.append(t_ekum)

        buffer_copy(ekum, t_ekum)


    if case_type == 1:

        ekum = get_cache (Ekum, {"eknr": [(eq, int1)]})

        if ekum:
            assign_it()
    elif case_type == 2:

        for ekum in db_session.query(Ekum).order_by(Ekum._recid).all():
            assign_it()
    elif case_type == 3:

        ekum = get_cache (Ekum, {"bezeich": [(eq, char1)],"eknr": [(ne, int1)]})

        if ekum:
            assign_it()

    return generate_output()