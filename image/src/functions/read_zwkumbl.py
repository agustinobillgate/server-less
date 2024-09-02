from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zwkum

def read_zwkumbl(case_type:int, int1:int, int2:int, int3:int, char1:str, char2:str, log1:bool, log2:bool):
    t_zwkum_list = []
    zwkum = None

    t_zwkum = None

    t_zwkum_list, T_zwkum = create_model_like(Zwkum)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zwkum_list, zwkum


        nonlocal t_zwkum
        nonlocal t_zwkum_list
        return {"t-zwkum": t_zwkum_list}

    def assign_it():

        nonlocal t_zwkum_list, zwkum


        nonlocal t_zwkum
        nonlocal t_zwkum_list


        t_zwkum = T_zwkum()
        t_zwkum_list.append(t_zwkum)

        buffer_copy(zwkum, t_zwkum)

    if case_type == 1:

        zwkum = db_session.query(Zwkum).filter(
                (Zwkum.zknr == int1) &  (Zwkum.departement == int2)).first()

        if zwkum:
            assign_it()
    elif case_type == 2:

        for zwkum in db_session.query(Zwkum).filter(
                (Zwkum.departement == int1)).all():
            assign_it()
    elif case_type == 3:

        zwkum = db_session.query(Zwkum).filter(
                (Zwkum.zknr != int1) &  (Zwkum.departement == int2) &  (func.lower(Zwkum.bezeich) == (char1).lower())).first()

        if zwkum:
            assign_it()

    return generate_output()