from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Ekum

def read_ekumbl(case_type:int, int1:int, int2:int, char1:str, char2:str):
    t_ekum_list = []
    ekum = None

    t_ekum = None

    t_ekum_list, T_ekum = create_model_like(Ekum)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ekum_list, ekum


        nonlocal t_ekum
        nonlocal t_ekum_list
        return {"t-ekum": t_ekum_list}

    def assign_it():

        nonlocal t_ekum_list, ekum


        nonlocal t_ekum
        nonlocal t_ekum_list


        t_ekum = T_ekum()
        t_ekum_list.append(t_ekum)

        buffer_copy(ekum, t_ekum)

    if case_type == 1:

        ekum = db_session.query(Ekum).filter(
                (Ekum.eknr == int1)).first()

        if ekum:
            assign_it()
    elif case_type == 2:

        for ekum in db_session.query(Ekum).all():
            assign_it()
    elif case_type == 3:

        ekum = db_session.query(Ekum).filter(
                (func.lower(Ekum.bezeich) == (char1).lower()) &  (Ekum.eknr != int1)).first()

        if ekum:
            assign_it()

    return generate_output()