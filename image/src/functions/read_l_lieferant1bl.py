from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant

def read_l_lieferant1bl(case_type:int, char1:str, int1:int):
    t_l_lieferant_list = []
    l_lieferant = None

    t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lieferant_list, l_lieferant


        nonlocal t_l_lieferant
        nonlocal t_l_lieferant_list
        return {"t-l-lieferant": t_l_lieferant_list}

    if case_type == 1:

        for l_lieferant in db_session.query(L_lieferant).filter(
                (func.lower(L_lieferant.firma) >= (char1).lower())).all():
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_list.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)
    elif case_type == 2:

        for l_lieferant in db_session.query(L_lieferant).filter(
                (L_lieferant.firma.op("~")(".*" + char1 + ".*"))).all():
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_list.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)

    return generate_output()