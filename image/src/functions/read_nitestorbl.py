from functions.additional_functions import *
import decimal
from models import Nitestor

def read_nitestorbl(case_type:int, int1:int, int2:int, int3:int, int4:int, char1:str):
    t_nitestor_list = []
    nitestor = None

    t_nitestor = None

    t_nitestor_list, T_nitestor = create_model_like(Nitestor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nitestor_list, nitestor


        nonlocal t_nitestor
        nonlocal t_nitestor_list
        return {"t-nitestor": t_nitestor_list}

    if case_type == 1:

        for nitestor in db_session.query(Nitestor).filter(
                (Nitestor.reihenfolge == int1)).all():
            t_nitestor = T_nitestor()
            t_nitestor_list.append(t_nitestor)

            buffer_copy(nitestor, t_nitestor)
    elif case_type == 2:

        for nitestor in db_session.query(Nitestor).filter(
                (Nitestor.night_type == int1) &  (Nitestor.reihenfolge == int2)).all():
            t_nitestor = T_nitestor()
            t_nitestor_list.append(t_nitestor)

            buffer_copy(nitestor, t_nitestor)

    return generate_output()